-- =============================================================================
-- OJK/BI RAG Assistant — PostgreSQL Schema
-- =============================================================================

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Enable full-text search configuration for Indonesian
-- (using default 'simple' config as Bahasa Indonesia isn't built-in)
CREATE TEXT SEARCH CONFIGURATION IF NOT EXISTS indonesian (COPY = simple);

-- -----------------------------------------------------------------------------
-- Regulatory document chunks (vector store)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS regulatory_chunks (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_document TEXT NOT NULL,
    document_type   TEXT NOT NULL CHECK (document_type IN ('POJK', 'SE OJK', 'PBI', 'PADG', 'Panduan', 'Statistik')),
    pasal           TEXT,
    bab             TEXT,
    tahun_terbit    TEXT,
    topik           TEXT,
    bahasa          TEXT DEFAULT 'id',
    content         TEXT NOT NULL,
    char_count      INTEGER,
    embedding       vector(768),
    content_tsv     tsvector GENERATED ALWAYS AS (to_tsvector('indonesian', content)) STORED,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- HNSW index for fast approximate nearest neighbor vector search
CREATE INDEX IF NOT EXISTS idx_chunks_embedding
    ON regulatory_chunks USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

-- GIN index for full-text search
CREATE INDEX IF NOT EXISTS idx_chunks_fts
    ON regulatory_chunks USING gin(content_tsv);

-- -----------------------------------------------------------------------------
-- Conversation logging (monitoring)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS conversations (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question        TEXT NOT NULL,
    answer          TEXT,
    model           TEXT,
    prompt_version  TEXT,
    input_tokens    INTEGER,
    output_tokens   INTEGER,
    cost            NUMERIC(10, 6),
    source_docs     JSONB,
    feedback        TEXT CHECK (feedback IN ('thumbs_up', 'thumbs_down') OR feedback IS NULL),
    judge_score     TEXT CHECK (judge_score IN ('good', 'bad', 'neutral') OR judge_score IS NULL),
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_conversations_created
    ON conversations (created_at DESC);

CREATE INDEX IF NOT EXISTS idx_conversations_feedback
    ON conversations (feedback);

CREATE INDEX IF NOT EXISTS idx_conversations_judge
    ON conversations (judge_score);
