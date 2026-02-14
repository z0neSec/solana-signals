"""Processing package for signal analysis."""
from .embeddings import embed_signals
from .clustering import cluster_signals
from .scoring import score_narratives
from .ideas import generate_build_ideas

__all__ = ["embed_signals", "cluster_signals", "score_narratives", "generate_build_ideas"]
