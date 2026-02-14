"""
Pydantic models for API requests and responses.
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: str
    version: str
    database: Optional[str] = None
    mode: Optional[str] = None


class PeriodInfo(BaseModel):
    """Time period information."""
    start: str
    end: str
    label: str


class DashboardSummary(BaseModel):
    """Dashboard summary statistics."""
    total_narratives: int
    new_narratives: int
    accelerating: int
    total_signals: int
    total_build_ideas: int
    data_sources: Optional[int] = None


class BuildIdea(BaseModel):
    """Product build idea."""
    title: str
    description: Optional[str] = None
    problem: Optional[str] = None
    solution: Optional[str] = None
    business_model: Optional[str] = None
    effort: Optional[str] = None
    market_size: Optional[str] = None


class EntitySet(BaseModel):
    """Key entities in a narrative."""
    programs: list[str] = []
    repos: list[str] = []
    kols: list[str] = []


class Evidence(BaseModel):
    """Evidence item for a narrative."""
    signal_id: Optional[str] = None
    domain: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    signal: Optional[str] = None
    metric: Optional[str] = None
    trend: Optional[str] = None
    link: Optional[str] = None


class NarrativeScores(BaseModel):
    """Scoring breakdown for a narrative."""
    domain_breakdown: dict[str, float]
    freshness: float
    novelty_bonus: float
    base_score: float
    final_score: float


class NarrativeResponse(BaseModel):
    """Full narrative response."""
    model_config = {"extra": "ignore"}

    id: str
    rank: int
    label: str
    status: str
    confidence: float
    summary: str
    signal_count: int
    domains: list[str]
    domain_counts: dict[str, int]
    first_seen: str
    last_seen: str
    scores: Optional[dict] = None
    build_ideas: list[BuildIdea] = []
    entities: Optional[dict] = None
    evidence: Optional[list[dict]] = None
    why_now: Optional[str] = None
    comparable_precedent: Optional[str] = None
    signals: Optional[list[dict]] = None


class NarrativeListResponse(BaseModel):
    """List of narratives response."""
    narratives: list[NarrativeResponse]
    total: int
    filters_applied: dict


class DashboardResponse(BaseModel):
    """Full dashboard response."""
    period: PeriodInfo
    narratives: list[NarrativeResponse]
    summary: DashboardSummary
    last_updated: str


class DataSource(BaseModel):
    """Data source information."""
    name: str
    provider: str
    update_frequency: str
    signals: list[str]


class ScoringWeights(BaseModel):
    """Scoring weight configuration."""
    domain_weights: dict[str, float]
    confidence_components: dict[str, float]
    formula: str


class ClusteringConfig(BaseModel):
    """Clustering configuration."""
    algorithm: str
    min_cluster_size: int
    cross_domain_requirement: bool
    embedding_model: str


class FilteringConfig(BaseModel):
    """Filtering configuration."""
    bot_detection: list[str]
    hype_filtering: list[str]
    quality_thresholds: dict[str, float | int]


class MethodologyResponse(BaseModel):
    """Methodology documentation response."""
    overview: str
    data_sources: list[DataSource]
    scoring: ScoringWeights
    clustering: ClusteringConfig
    filtering: FilteringConfig
