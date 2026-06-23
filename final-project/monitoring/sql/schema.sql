-- OJK/BI Regulatory Intelligence Assistant
-- Database Schema

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- ─────────────────────────────────────────
-- Chunks table (vector store)
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS chunks (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_document TEXT NOT NULL,
    document_type   TEXT NOT NULL CHECK (document_type IN ('POJK', 'SE OJK', 'PBI', 'PADG', 'Panduan')),
    pasal           TEXT,
    bab             TEXT,
    tahun_terbit    TEXT,
    topik           TEXT,
    bahasa          TEXT DEFAULT 'id' CHECK (bahasa IN ('id', 'en')),
    content         TEXT NOT NULL,
    char_count      INTEGER,
    embedding       vector(768),  -- intfloat/multilingual-e5-base
    tsvector_content tsvector,    -- for FTS keyword search
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- HNSW index for fast vector search
CREATE INDEX IF NOT EXISTS chunks_embedding_hnsw_idx
    ON chunks USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

-- GIN index for full-text search
CREATE INDEX IF NOT EXISTS chunks_tsvector_idx
    ON chunks USING gin(tsvector_content);

-- Trigger to auto-update tsvector
CREATE OR REPLACE FUNCTION update_tsvector()
RETURNS TRIGGER AS $$
BEGIN
    NEW.tsvector_content := to_tsvector('indonesian', COALESCE(NEW.content, ''));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER chunks_tsvector_update
    BEFORE INSERT OR UPDATE ON chunks
    FOR EACH ROW EXECUTE FUNCTION update_tsvector();

-- ─────────────────────────────────────────
-- Conversations table (monitoring)
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS conversations (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question        TEXT NOT NULL,
    answer          TEXT,
    model           TEXT,
    prompt_version  TEXT DEFAULT 'v1',
    input_tokens    INTEGER,
    output_tokens   INTEGER,
    cost            NUMERIC(10, 6),
    source_docs     JSONB,  -- [{"source_document": "...", "pasal": "..."}]
    feedback        TEXT CHECK (feedback IN ('thumbs_up', 'thumbs_down')),
    judge_score     TEXT CHECK (judge_score IN ('good', 'bad', 'neutral')),
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS conversations_created_at_idx
    ON conversations (created_at DESC);
