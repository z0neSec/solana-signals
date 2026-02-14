"""
Narrative scoring and ranking.

Calculates confidence scores and ranks narratives.
"""
import logging
import math
from typing import Any
from datetime import datetime, timedelta, timezone
from config import DOMAIN_WEIGHTS

logger = logging.getLogger(__name__)


def _parse_dt(dt_str: str) -> datetime:
    """Parse a datetime string to a timezone-aware datetime."""
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    except Exception:
        dt = datetime.now(timezone.utc)
    # Ensure timezone-aware
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def calculate_domain_score(narrative: dict[str, Any]) -> dict[str, float]:
    """Calculate per-domain contribution scores."""
    domain_counts = narrative["domain_counts"]
    total = sum(domain_counts.values())
    
    scores = {}
    for domain, count in domain_counts.items():
        # Normalize by total and apply domain weight
        weight = DOMAIN_WEIGHTS.get(domain, 0.2)
        scores[domain] = (count / total) * weight
    
    return scores


def calculate_freshness(narrative: dict[str, Any]) -> float:
    """
    Calculate freshness weight based on most recent signal.
    
    Returns value between 0.5 and 1.0.
    """
    try:
        last_seen = _parse_dt(narrative["last_seen"])
        now = datetime.now(timezone.utc)
        hours_old = (now - last_seen).total_seconds() / 3600
        
        # Linear decay: 1.0 at 0 hours, 0.5 at 168 hours (7 days)
        freshness = max(0.5, 1 - (hours_old / 168))
        return freshness
    except Exception:
        return 0.75  # Default middle value


def calculate_novelty_bonus(narrative: dict[str, Any], existing_narratives: list = None) -> float:
    """
    Calculate novelty bonus for first-time narratives.
    
    Returns 1.5 for new narratives, 1.0 for known ones.
    """
    # For now, assume all narratives in this fortnight are potentially new
    # In production, compare against historical narrative database
    
    first_seen = _parse_dt(narrative["first_seen"])
    now = datetime.now(timezone.utc)
    days_since_first = (now - first_seen).days
    
    # If first seen in last 7 days, give novelty bonus
    if days_since_first <= 7:
        return 1.5
    return 1.0


def calculate_credibility(narrative: dict[str, Any]) -> float:
    """Calculate average credibility from source signals."""
    signals = narrative["signals"]
    if not signals:
        return 0.5
    
    total_credibility = sum(s.get("credibility_score", 0.5) for s in signals)
    return total_credibility / len(signals)


def calculate_confidence(narrative: dict[str, Any]) -> float:
    """
    Calculate overall confidence score for a narrative.
    
    Components:
    - Domain coverage (25%)
    - Temporal consistency (25%)
    - Source credibility (20%)
    - Signal volume (15%)
    - Novelty (15%)
    """
    # Domain coverage: how many domains are represented
    domain_count = len(narrative["domains"])
    domain_coverage = min(1.0, domain_count / 3) * 0.25
    
    # Temporal consistency: signals spread over time
    first_seen = _parse_dt(narrative["first_seen"])
    last_seen = _parse_dt(narrative["last_seen"])
    duration_days = max(1, (last_seen - first_seen).days)
    temporal_consistency = min(1.0, duration_days / 14) * 0.25
    
    # Source credibility
    credibility = calculate_credibility(narrative) * 0.20
    
    # Signal volume (log scale, max at ~50 signals)
    import math
    signal_count = narrative["signal_count"]
    volume_score = min(1.0, math.log(signal_count + 1) / math.log(50)) * 0.15
    
    # Novelty
    novelty = (1.0 if calculate_novelty_bonus(narrative) > 1.0 else 0.5) * 0.15
    
    confidence = domain_coverage + temporal_consistency + credibility + volume_score + novelty
    return round(confidence, 2)


async def score_narratives(narratives: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Score and rank all narratives.
    
    Args:
        narratives: List of narrative objects from clustering
        
    Returns:
        Scored and ranked narratives
    """
    logger.info(f"Scoring {len(narratives)} narratives...")
    
    for narrative in narratives:
        # Calculate component scores
        domain_scores = calculate_domain_score(narrative)
        freshness = calculate_freshness(narrative)
        novelty = calculate_novelty_bonus(narrative)
        confidence = calculate_confidence(narrative)
        
        # Combined narrative score
        base_score = sum(domain_scores.values())
        final_score = base_score * freshness * novelty
        
        # Add scoring details to narrative
        narrative["scores"] = {
            "domain_breakdown": domain_scores,
            "freshness": freshness,
            "novelty_bonus": novelty,
            "base_score": base_score,
            "final_score": round(final_score, 3)
        }
        narrative["confidence"] = confidence
        
        # Determine status
        if novelty > 1.0:
            narrative["status"] = "NEW"
        elif freshness > 0.7:
            narrative["status"] = "ACCELERATING"
        else:
            narrative["status"] = "STABLE"
    
    # Sort by final score (descending)
    narratives.sort(key=lambda n: n["scores"]["final_score"], reverse=True)
    
    # Add rank
    for i, narrative in enumerate(narratives):
        narrative["rank"] = i + 1
    
    logger.info(f"Scored and ranked {len(narratives)} narratives")
    return narratives
