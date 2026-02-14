-- =============================================
-- Solana Signals Database Schema for Supabase
-- Run this in the Supabase SQL Editor
-- =============================================

-- Enable pgvector extension (for embeddings)
CREATE EXTENSION IF NOT EXISTS vector;

-- Fortnights table (create first due to foreign key)
CREATE TABLE IF NOT EXISTS fortnights (
    id TEXT PRIMARY KEY,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Narratives table
CREATE TABLE IF NOT EXISTS narratives (
    id TEXT PRIMARY KEY,
    label TEXT NOT NULL,
    summary TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('NEW', 'ACCELERATING', 'STABLE', 'DECLINING')),
    confidence FLOAT NOT NULL CHECK (confidence >= 0 AND confidence <= 100),
    rank INTEGER NOT NULL,
    signal_count INTEGER NOT NULL DEFAULT 0,
    domains TEXT[] NOT NULL DEFAULT '{}',
    domain_counts JSONB NOT NULL DEFAULT '{}',
    first_seen TIMESTAMPTZ NOT NULL,
    last_seen TIMESTAMPTZ NOT NULL,
    scores JSONB NOT NULL DEFAULT '{}',
    build_ideas JSONB NOT NULL DEFAULT '[]',
    entities JSONB NOT NULL DEFAULT '{}',
    evidence JSONB DEFAULT '[]',
    why_now TEXT,
    comparable_precedent TEXT,
    fortnight_start DATE NOT NULL,
    keywords TEXT[] DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Signals table
CREATE TABLE IF NOT EXISTS signals (
    id TEXT PRIMARY KEY,
    domain TEXT NOT NULL CHECK (domain IN ('onchain', 'github', 'social', 'news', 'discord')),
    type TEXT NOT NULL,
    description TEXT NOT NULL,
    author TEXT,
    source TEXT,
    url TEXT,
    timestamp TIMESTAMPTZ NOT NULL,
    credibility_score FLOAT NOT NULL DEFAULT 0.5,
    relevance_score FLOAT DEFAULT 0.5,
    metadata JSONB DEFAULT '{}',
    embedding vector(1536),
    narrative_id TEXT REFERENCES narratives(id) ON DELETE SET NULL,
    processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_signals_domain ON signals(domain);
CREATE INDEX IF NOT EXISTS idx_signals_type ON signals(type);
CREATE INDEX IF NOT EXISTS idx_signals_timestamp ON signals(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_signals_narrative ON signals(narrative_id);
CREATE INDEX IF NOT EXISTS idx_signals_processed ON signals(processed);
CREATE INDEX IF NOT EXISTS idx_narratives_status ON narratives(status);
CREATE INDEX IF NOT EXISTS idx_narratives_fortnight ON narratives(fortnight_start);
CREATE INDEX IF NOT EXISTS idx_narratives_rank ON narratives(rank);
CREATE INDEX IF NOT EXISTS idx_narratives_confidence ON narratives(confidence DESC);

-- Vector similarity index (create after data is inserted for better performance)
-- CREATE INDEX IF NOT EXISTS idx_signals_embedding ON signals USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger for narratives updated_at
DROP TRIGGER IF EXISTS update_narratives_updated_at ON narratives;
CREATE TRIGGER update_narratives_updated_at
    BEFORE UPDATE ON narratives
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Row Level Security (RLS) - Enable for production
ALTER TABLE signals ENABLE ROW LEVEL SECURITY;
ALTER TABLE narratives ENABLE ROW LEVEL SECURITY;
ALTER TABLE fortnights ENABLE ROW LEVEL SECURITY;

-- Public read access policies (adjust for production)
CREATE POLICY "Allow public read access on signals" ON signals
    FOR SELECT USING (true);

CREATE POLICY "Allow public read access on narratives" ON narratives
    FOR SELECT USING (true);

CREATE POLICY "Allow public read access on fortnights" ON fortnights
    FOR SELECT USING (true);

-- Service role full access (for backend)
CREATE POLICY "Allow service role full access on signals" ON signals
    FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Allow service role full access on narratives" ON narratives
    FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Allow service role full access on fortnights" ON fortnights
    FOR ALL USING (auth.role() = 'service_role');

-- =============================================
-- Views for easier querying
-- =============================================

-- Dashboard summary view
CREATE OR REPLACE VIEW dashboard_summary AS
SELECT 
    (SELECT COUNT(*) FROM narratives WHERE fortnight_start >= CURRENT_DATE - INTERVAL '14 days') as active_narratives,
    (SELECT COUNT(*) FROM signals WHERE timestamp >= CURRENT_DATE - INTERVAL '14 days') as signals_processed,
    (SELECT COUNT(DISTINCT domain) FROM signals WHERE timestamp >= CURRENT_DATE - INTERVAL '14 days') as data_sources,
    (SELECT AVG(confidence) FROM narratives WHERE fortnight_start >= CURRENT_DATE - INTERVAL '14 days') as avg_confidence;

-- Top narratives view
CREATE OR REPLACE VIEW top_narratives AS
SELECT 
    id,
    label,
    summary,
    status,
    confidence,
    rank,
    signal_count,
    domains,
    keywords,
    first_seen,
    last_seen,
    fortnight_start,
    created_at,
    updated_at
FROM narratives
WHERE fortnight_start >= CURRENT_DATE - INTERVAL '14 days'
ORDER BY rank ASC, confidence DESC
LIMIT 10;

-- Recent signals view
CREATE OR REPLACE VIEW recent_signals AS
SELECT 
    s.id,
    s.domain,
    s.type,
    s.description,
    s.author,
    s.source,
    s.timestamp,
    s.relevance_score,
    s.narrative_id,
    n.label as narrative_label
FROM signals s
LEFT JOIN narratives n ON s.narrative_id = n.id
WHERE s.timestamp >= CURRENT_DATE - INTERVAL '14 days'
ORDER BY s.timestamp DESC
LIMIT 100;

-- =============================================
-- Sample data (remove in production)
-- =============================================

-- Insert current fortnight
INSERT INTO fortnights (id, start_date, end_date, status)
VALUES (
    'fortnight_' || TO_CHAR(CURRENT_DATE, 'YYYY_MM_DD'),
    CURRENT_DATE - INTERVAL '14 days',
    CURRENT_DATE,
    'active'
) ON CONFLICT (id) DO NOTHING;

-- Success message
SELECT 'Schema created successfully!' as message;
