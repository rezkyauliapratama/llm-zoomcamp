#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# LLM Zoomcamp — Module 03: AI Orchestration with Kestra
# =============================================================================
# One-command setup: source .env, base64-encode secrets, start Kestra, import flows
# Usage:
#   chmod +x setup.sh
#   ./setup.sh
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# ── Step 1: Load API keys from .env ─────────────────────────────────────
if [ -f .env ]; then
    set -a
    source .env
    set +a
    echo "✓ Loaded .env"
else
    echo "✗ .env not found. Copy .env.template to .env and fill in your API keys."
    exit 1
fi

# ── Step 2: Validate required keys ──────────────────────────────────────
MISSING=0
for var in GEMINI_API_KEY OPENROUTER_API_KEY TAVILY_API_KEY; do
    if [ -z "${!var:-}" ] || [ "${!var:-}" = "your-${var,,}-key-here" ]; then
        echo "✗ $var is not set in .env"
        MISSING=1
    fi
done

if [ "$MISSING" -eq 1 ]; then
    echo "Please update your .env file and re-run."
    exit 1
fi

# ── Step 3: Base64-encode secrets for Kestra ────────────────────────────
export SECRET_GEMINI_API_KEY=$(echo -n "$GEMINI_API_KEY" | base64)
export SECRET_OPENROUTER_API_KEY=$(echo -n "$OPENROUTER_API_KEY" | base64)
export SECRET_TAVILY_API_KEY=$(echo -n "$TAVILY_API_KEY" | base64)

echo "✓ Secrets encoded"

# ── Step 4: Start Kestra ────────────────────────────────────────────────
echo "Starting Kestra..."
docker compose up -d

echo "Waiting for Kestra to be ready..."
sleep 10

echo ""
echo "============================================="
echo "  Kestra UI: http://localhost:8080"
echo "  Login:     admin@kestra.io / Admin1234!"
echo "============================================="
echo ""
echo "Next steps:"
echo "  1. Open Kestra UI and click 'Flows'"
echo "  2. Import each flow from the flows/ directory"
echo "  3. Or use the API:"
echo ""

# Import flows via Kestra API
for flow in flows/*.yaml; do
    fname=$(basename "$flow")
    echo "  curl -X POST -u 'admin@kestra.io:Admin1234!'"
    echo "    http://localhost:8080/api/v1/flows/import"
    echo "    -F fileUpload=@flows/$fname"
done

echo ""
echo "✓ Setup complete!"
