"""
API route definitions with live Supabase data.
"""
from fastapi import APIRouter, HTTPException, Query
from datetime import datetime, timedelta
from typing import Optional, List

from .models import (
    DashboardResponse,
    NarrativeResponse,
    NarrativeListResponse,
    MethodologyResponse,
    HealthResponse
)

router = APIRouter()


def get_db():
    """Get database repositories."""
    from db.supabase import NarrativeRepository, SignalRepository, DashboardRepository
    return {
        "narratives": NarrativeRepository,
        "signals": SignalRepository,
        "dashboard": DashboardRepository
    }


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    db_status = "connected"
    try:
        from db.supabase import init_db
        if not init_db():
            db_status = "disconnected"
    except Exception:
        db_status = "disconnected"
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "database": db_status,
        "mode": "live"
    }


@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard():
    """Get dashboard overview with all narratives."""
    try:
        db = get_db()
        summary = db["dashboard"].get_summary()
        narratives = db["narratives"].get_current_fortnight(limit=10)
        
        # If DB is empty, try in-memory cache
        if not narratives:
            from processing.pipeline import get_cached_narratives
            narratives = get_cached_narratives()
        
        now = datetime.now()
        fortnight_start = now - timedelta(days=14)

        # Count statuses
        status_counts = {}
        for n in narratives:
            s = n.get("status", "NEW")
            status_counts[s] = status_counts.get(s, 0) + 1
        
        return {
            "period": {
                "start": fortnight_start.strftime("%Y-%m-%d"),
                "end": now.strftime("%Y-%m-%d"),
                "label": f"{fortnight_start.strftime('%B %d')} – {now.strftime('%B %d, %Y')}"
            },
            "narratives": narratives,
            "summary": {
                "total_narratives": len(narratives),
                "new_narratives": status_counts.get("NEW", 0),
                "accelerating": status_counts.get("ACCELERATING", 0),
                "total_signals": sum(n.get("signal_count", 0) for n in narratives),
                "data_sources": len(set(d for n in narratives for d in n.get("domains", []))),
                "total_build_ideas": sum(len(n.get("build_ideas", [])) for n in narratives)
            },
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load dashboard: {str(e)}")


@router.get("/narratives", response_model=NarrativeListResponse)
async def list_narratives(
    status: Optional[str] = None,
    min_confidence: Optional[float] = None,
    limit: int = Query(default=10, ge=1, le=50),
    offset: int = Query(default=0, ge=0)
):
    """List narratives with optional filtering."""
    try:
        db = get_db()
        narratives = db["narratives"].get_all(
            status=status,
            min_confidence=min_confidence,
            limit=limit,
            offset=offset
        )
        
        # If DB is empty, try in-memory cache
        if not narratives:
            from processing.pipeline import get_cached_narratives
            narratives = get_cached_narratives()
            # Apply filters on cached data
            if status:
                narratives = [n for n in narratives if n.get("status") == status.upper()]
            if min_confidence is not None:
                narratives = [n for n in narratives if n.get("confidence", 0) >= min_confidence]
            narratives = narratives[offset : offset + limit]
        
        return {
            "narratives": narratives,
            "total": len(narratives),
            "filters_applied": {
                "status": status,
                "min_confidence": min_confidence,
                "limit": limit,
                "offset": offset
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load narratives: {str(e)}")


@router.get("/narratives/{narrative_id}", response_model=NarrativeResponse)
async def get_narrative(narrative_id: str):
    """Get detailed view of a specific narrative."""
    try:
        db = get_db()
        narrative = db["narratives"].get_with_signals(narrative_id)
        if narrative:
            return narrative

        # Try in-memory cache
        from processing.pipeline import get_cached_narratives
        for n in get_cached_narratives():
            if n.get("id") == narrative_id:
                return n

        raise HTTPException(status_code=404, detail="Narrative not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load narrative: {str(e)}")


@router.get("/signals")
async def list_signals(
    domain: Optional[str] = None,
    narrative_id: Optional[str] = None,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0)
):
    """List signals with optional filtering."""
    try:
        db = get_db()
        
        if narrative_id:
            signals = db["signals"].get_by_narrative(narrative_id, limit=limit)
        else:
            signals = db["signals"].get_recent(days=14, limit=limit)
        
        # If DB is empty, try in-memory cache
        if not signals:
            from processing.pipeline import get_cached_signals
            signals = get_cached_signals()
            if narrative_id:
                signals = [s for s in signals if s.get("narrative_id") == narrative_id]

        # Filter by domain if specified
        if domain:
            signals = [s for s in signals if s.get("domain") == domain]
        
        # Strip embeddings from response
        clean = []
        for s in signals:
            clean.append({k: v for k, v in s.items() if k != "embedding"})

        return {
            "signals": clean[offset : offset + limit],
            "total": len(clean),
            "filters_applied": {
                "domain": domain,
                "narrative_id": narrative_id,
                "limit": limit,
                "offset": offset
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load signals: {str(e)}")


@router.get("/methodology", response_model=MethodologyResponse)
async def get_methodology():
    """Get detailed methodology documentation."""
    return {
        "overview": "Solana Signal Intelligence monitors onchain activity, developer momentum, and social signals to surface emerging narratives fortnightly.",
        "data_sources": [
            {
                "name": "Onchain",
                "provider": "Helius API",
                "update_frequency": "Hourly",
                "signals": ["New program deployments", "Transaction spikes", "Wallet cohort behavior"]
            },
            {
                "name": "GitHub",
                "provider": "GitHub GraphQL API",
                "update_frequency": "Every 6 hours",
                "signals": ["New repositories", "Star/fork growth", "Commit velocity"]
            },
            {
                "name": "Social",
                "provider": "Twitter API v2",
                "update_frequency": "Every 4 hours",
                "signals": ["KOL discussions", "Technical threads", "Announcements"]
            }
        ],
        "scoring": {
            "domain_weights": {
                "onchain": 0.40,
                "github": 0.35,
                "social": 0.25
            },
            "confidence_components": {
                "domain_coverage": 0.25,
                "temporal_consistency": 0.25,
                "source_credibility": 0.20,
                "signal_volume": 0.15,
                "novelty": 0.15
            },
            "formula": "narrative_score = (onchain × 0.40 + github × 0.35 + social × 0.25) × freshness × novelty_bonus"
        },
        "clustering": {
            "algorithm": "HDBSCAN",
            "min_cluster_size": 5,
            "cross_domain_requirement": True,
            "embedding_model": "text-embedding-3-small"
        },
        "filtering": {
            "bot_detection": ["Wallet age", "Transaction timing entropy", "Funding patterns"],
            "hype_filtering": ["Micro-transaction filtering", "Single-program cluster detection"],
            "quality_thresholds": {
                "min_signals": 3,
                "min_duration_days": 1,
                "min_confidence": 0.3
            }
        }
    }


@router.get("/export/markdown")
async def export_markdown():
    """Export current narratives as Markdown document."""
    try:
        db = get_db()
        narratives = db["narratives"].get_current_fortnight(limit=20)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export: {str(e)}")
    
    now = datetime.now()
    fortnight_start = now - timedelta(days=14)
    
    md = "# Solana Signal Intelligence Report\n\n"
    md += f"**Period**: {fortnight_start.strftime('%B %d')} – {now.strftime('%B %d, %Y')}\n"
    md += f"**Generated**: {now.strftime('%Y-%m-%d %H:%M')}\n\n"
    md += "---\n\n"
    
    for narrative in narratives:
        status_emoji = {"NEW": "🆕", "ACCELERATING": "📈", "STABLE": "➡️", "DECLINING": "📉"}.get(narrative.get("status"), "")
        confidence_pct = int(narrative.get("confidence", 0) * 100) if narrative.get("confidence", 0) <= 1 else int(narrative.get("confidence", 0))
        
        md += f"## {status_emoji} {narrative.get('label', 'Unknown')}\n\n"
        md += f"**Status**: {narrative.get('status')} | **Confidence**: {confidence_pct}%\n\n"
        md += f"{narrative.get('summary', '')}\n\n"
        
        if narrative.get("build_ideas"):
            md += "### Build Ideas\n\n"
            for idea in narrative.get("build_ideas", []):
                md += f"**{idea.get('title')}**\n"
                md += f"- Problem: {idea.get('problem')}\n"
                md += f"- Effort: {idea.get('effort')}\n\n"
        
        md += "---\n\n"
    
    return {"markdown": md, "generated_at": datetime.now().isoformat()}


@router.post("/ingest/trigger")
async def trigger_ingestion():
    """Manually trigger data ingestion (for testing)."""
    try:
        from ingestors.coordinator import run_ingestion_pipeline
        result = await run_ingestion_pipeline()
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")


@router.post("/process/trigger")
async def trigger_processing():
    """Manually trigger narrative processing (for testing)."""
    try:
        from processing.pipeline import run_processing_pipeline
        result = await run_processing_pipeline()
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@router.post("/pipeline/trigger")
async def trigger_full_pipeline():
    """Run full pipeline: ingest → embed → cluster → score → enrich → save."""
    try:
        from processing.pipeline import run_full_pipeline
        result = await run_full_pipeline()
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline failed: {str(e)}")
