# Deployment

## Local (Docker Compose) — Required for Base Score

All services run via `docker-compose.yml` at the project root:

```bash
cd final-project
cp .env.example .env  # Configure your API keys
docker compose up -d
```

Service URLs:
- Open WebUI: http://localhost:3000
- N8N: http://localhost:5678
- Grafana: http://localhost:3001
- PostgreSQL: localhost:5432

## Cloud Deployment (GCP) — Bonus +2 Points

Target: **GCP Cloud Run** + **Cloud SQL** (PostgreSQL with pgvector)

```
Cloud Run         → Open WebUI container (stateless, auto-scaling)
Cloud Run         → N8N container
Cloud SQL (PG17)  → PostgreSQL + pgvector extension
Artifact Registry → Docker images
Secret Manager    → API keys, DB credentials
Cloud Scheduler   → Trigger N8N weekly ingestion
```

Region: `asia-southeast1` (Singapore, lowest latency from Indonesia)

### GCP Deployment Steps

1. Build and push Docker images to Artifact Registry
2. Create Cloud SQL instance with pgvector extension
3. Store secrets in Secret Manager
4. Deploy services to Cloud Run
5. Configure Cloud Scheduler for weekly ingestion trigger

See `gcp/` directory for Terraform configs (if implemented).
