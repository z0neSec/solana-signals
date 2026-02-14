"""
Database models and schema.

Uses Supabase PostgreSQL with pgvector for embeddings.
"""
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class Signal:
    """Raw signal from any data source."""
    id: str
    domain: str  # onchain, github, social
    type: str  # new_program, commit_velocity, kol_tweet, etc.
    description: str
    timestamp: datetime
    credibility_score: float
    metadata: dict = field(default_factory=dict)
    embedding: Optional[list[float]] = None
    narrative_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Narrative:
    """Detected narrative cluster."""
    id: str
    label: str
    summary: str
    status: str  # NEW, ACCELERATING, STABLE
    confidence: float
    rank: int
    signal_count: int
    domains: list[str]
    domain_counts: dict[str, int]
    first_seen: datetime
    last_seen: datetime
    scores: dict
    build_ideas: list[dict]
    entities: dict
    evidence: list[dict]
    why_now: Optional[str] = None
    comparable_precedent: Optional[str] = None
    fortnight_start: datetime = None
    created_at: datetime = field(default_factory=datetime.now)


# Base class for SQLAlchemy if needed
class Base:
    """Base class placeholder for ORM."""
    pass


# SQL Schema for Supabase
SQL_SCHEMA = """
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Signals table
CREATE TABLE IF NOT EXISTS signals (
    id TEXT PRIMARY KEY,
    domain TEXT NOT NULL,
    type TEXT NOT NULL,
    description TEXT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    credibility_score FLOAT NOT NULL,
    metadata JSONB DEFAULT '{}',
    embedding vector(1536),
    narrative_id TEXT REFERENCES narratives(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Narratives table
CREATE TABLE IF NOT EXISTS narratives (
    id TEXT PRIMARY KEY,
    label TEXT NOT NULL,
    summary TEXT NOT NULL,
    status TEXT NOT NULL,
    confidence FLOAT NOT NULL,
    rank INTEGER NOT NULL,
    signal_count INTEGER NOT NULL,
    domains TEXT[] NOT NULL,
    domain_counts JSONB NOT NULL,
    first_seen TIMESTAMPTZ NOT NULL,
    last_seen TIMESTAMPTZ NOT NULL,
    scores JSONB NOT NULL,
    build_ideas JSONB NOT NULL,
    entities JSONB NOT NULL,
    evidence JSONB DEFAULT '[]',
    why_now TEXT,
    comparable_precedent TEXT,
    fortnight_start DATE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_signals_domain ON signals(domain);
CREATE INDEX IF NOT EXISTS idx_signals_timestamp ON signals(timestamp);
CREATE INDEX IF NOT EXISTS idx_signals_narrative ON signals(narrative_id);
CREATE INDEX IF NOT EXISTS idx_narratives_status ON narratives(status);
CREATE INDEX IF NOT EXISTS idx_narratives_fortnight ON narratives(fortnight_start);
CREATE INDEX IF NOT EXISTS idx_signals_embedding ON signals USING ivfflat (embedding vector_cosine_ops);

-- Fortnight periods table for tracking
CREATE TABLE IF NOT EXISTS fortnights (
    id TEXT PRIMARY KEY,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMPTZ DEFAULT NOW()
);
"""
