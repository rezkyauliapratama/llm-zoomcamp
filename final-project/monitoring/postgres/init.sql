-- PostgreSQL initialization script
-- Creates pgvector extension, document chunks table, and conversations table

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Document chunks (knowledge base)
CREATE TABLE IF NOT EXISTS document_chunks (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_document TEXT NOT NULL,
    document_type   TEXT NOT NULL,  -- POJK | SE OJK | PBI | PADG | Panduan
    pasal           TEXT,
    bab             TEXT,
    tahun_terbit    TEXT,
    topik           TEXT,
    bahasa          TEXT DEFAULT 'id',
    content         TEXT NOT NULL,
    char_count      INTEGER GENERATED ALWAYS AS (LENGTH(content)) STORED,
    embedding       vector(768),  -- multilingual-e5-base dimensions
    content_tsv     tsvector GENERATED ALWAYS AS (to_tsvector('indonesian', content)) STORED,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- HNSW index for fast vector similarity search
CREATE INDEX IF NOT EXISTS document_chunks_embedding_idx
    ON document_chunks USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

-- GIN index for full-text search
CREATE INDEX IF NOT EXISTS document_chunks_tsv_idx
    ON document_chunks USING GIN (content_tsv);

-- Conversation logs (monitoring)
CREATE TABLE IF NOT EXISTS conversations (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question        TEXT NOT NULL,
    answer          TEXT NOT NULL,
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

-- Index for monitoring queries
CREATE INDEX IF NOT EXISTS conversations_created_at_idx
    ON conversations (created_at);

CREATE INDEX IF NOT EXISTS conversations_feedback_idx
    ON conversations (feedback);
