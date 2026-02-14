"""
Narrative clustering using HDBSCAN.

Groups signals into coherent narratives based on embedding similarity.
"""
import logging
from typing import Any
from datetime import datetime
import numpy as np
from collections import defaultdict

logger = logging.getLogger(__name__)

# Try to import HDBSCAN, fall back to simple clustering if not available
try:
    import hdbscan
    HAS_HDBSCAN = True
except ImportError:
    HAS_HDBSCAN = False
    logger.warning("HDBSCAN not available, using fallback clustering")


def simple_clustering(embeddings: np.ndarray, n_clusters: int = 5) -> np.ndarray:
    """
    Simple fallback clustering based on random assignment.
    In production, use HDBSCAN or K-means.
    """
    from sklearn.cluster import KMeans
    
    if len(embeddings) < n_clusters:
        return np.arange(len(embeddings))
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    return kmeans.fit_predict(embeddings)


def hdbscan_clustering(embeddings: np.ndarray, min_cluster_size: int = 5) -> np.ndarray:
    """
    HDBSCAN clustering for density-based narrative detection.
    """
    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=2,
        metric='euclidean',
        cluster_selection_method='eom'
    )
    return clusterer.fit_predict(embeddings)


async def cluster_signals(signals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Cluster signals into narratives.
    
    Args:
        signals: List of signals with embeddings
        
    Returns:
        List of narrative objects, each containing related signals
    """
    logger.info(f"Clustering {len(signals)} signals into narratives...")
    
    if not signals:
        return []
    
    # Extract embeddings matrix
    embeddings = np.array([s["embedding"] for s in signals])
    
    # Perform clustering
    if HAS_HDBSCAN and len(signals) >= 5:
        labels = hdbscan_clustering(embeddings, min_cluster_size=3)
    else:
        labels = simple_clustering(embeddings, n_clusters=min(5, len(signals)))
    
    # Group signals by cluster
    clusters = defaultdict(list)
    for i, label in enumerate(labels):
        if label >= 0:  # Ignore noise points (label=-1)
            clusters[label].append(signals[i])
    
    # Convert to narrative objects
    narratives = []
    for cluster_id, cluster_signals in clusters.items():
        # Check cross-domain requirement (signals from at least 2 domains)
        domains = set(s["domain"] for s in cluster_signals)
        
        if len(domains) < 2 and len(cluster_signals) >= 5:
            # Single domain but enough signals - still include but lower confidence
            cross_domain = False
        elif len(domains) >= 2:
            cross_domain = True
        else:
            continue  # Skip small single-domain clusters
        
        # Calculate domain breakdown
        domain_counts = defaultdict(int)
        for s in cluster_signals:
            domain_counts[s["domain"]] += 1
        
        narratives.append({
            "id": f"narrative_{cluster_id}_{datetime.now().strftime('%Y%m%d')}",
            "signals": cluster_signals,
            "signal_count": len(cluster_signals),
            "domains": list(domains),
            "domain_counts": dict(domain_counts),
            "cross_domain": cross_domain,
            "first_seen": min(s["timestamp"] for s in cluster_signals),
            "last_seen": max(s["timestamp"] for s in cluster_signals),
        })
    
    logger.info(f"Detected {len(narratives)} narrative clusters")
    return narratives


def validate_narrative(narrative: dict[str, Any]) -> bool:
    """
    Validate that a narrative meets quality thresholds.
    
    Returns True if narrative should be included in output.
    """
    # Must have at least 3 signals
    if narrative["signal_count"] < 3:
        return False
    
    # Must span at least 2 days
    try:
        from datetime import timezone as tz
        first_seen = datetime.fromisoformat(narrative["first_seen"].replace("Z", "+00:00"))
        last_seen = datetime.fromisoformat(narrative["last_seen"].replace("Z", "+00:00"))
        if first_seen.tzinfo is None:
            first_seen = first_seen.replace(tzinfo=tz.utc)
        if last_seen.tzinfo is None:
            last_seen = last_seen.replace(tzinfo=tz.utc)
        duration = (last_seen - first_seen).days
    except Exception:
        duration = 0
    
    if duration < 1 and not narrative["cross_domain"]:
        return False
    
    return True
