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

# -- Cleanup handler -------------------------------------------------------
cleanup() {
    echo ""
    echo "  Setup interrupted. Containers may still be running."
    echo "   Run 'docker compose down' to stop them."
}
trap cleanup EXIT

# -- Step 1: Load API keys from .env ---------------------------------------
if [ -f .env ]; then
    set -a
    source .env
    set +a
    echo "OK Loaded .env"
else
    echo "FAIL .env not found. Copy .env.template to .env and fill in your API keys."
    exit 1
fi

# -- Step 2: Validate required keys ----------------------------------------
MISSING=0
for var in GEMINI_API_KEY OPENROUTER_API_KEY TAVILY_API_KEY; do
    val="${!var:-}"
    lower=$(echo "$var" | tr '[:upper:]' '[:lower:]')
    placeholder="your-${lower}-key-here"
    if [ -z "$val" ] || [ "$val" = "$placeholder" ]; then
        echo "FAIL $var is not set in .env"
        MISSING=1
    fi
done

if [ "$MISSING" -eq 1 ]; then
    echo "Please update your .env file and re-run."
    exit 1
fi

# -- Step 3: Base64-encode secrets for Kestra ------------------------------
# NOTE: base64 is encoding, NOT encryption. Anyone with access to the
# container can decode these back to plaintext. Kestra requires this format
# for its internal secret store.
export SECRET_GEMINI_API_KEY=$(echo -n "$GEMINI_API_KEY" | base64)
export SECRET_OPENROUTER_API_KEY=$(echo -n "$OPENROUTER_API_KEY" | base64)
export SECRET_TAVILY_API_KEY=$(echo -n "$TAVILY_API_KEY" | base64)
echo "OK Secrets encoded"

# -- Step 4: Start Kestra --------------------------------------------------
echo "Starting Kestra..."
docker compose up -d

# -- Step 5: Wait for Kestra to be healthy ---------------------------------
echo "Waiting for Kestra to be ready..."
MAX_RETRIES=30
RETRY=0
while [ $RETRY -lt $MAX_RETRIES ]; do
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/ 2>/dev/null || echo "000")
    if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "302" ]; then
        echo "OK Kestra is ready (HTTP $HTTP_CODE)"
        break
    fi
    RETRY=$((RETRY + 1))
    sleep 3
done

if [ $RETRY -eq $MAX_RETRIES ]; then
    echo "FAIL Kestra did not become ready within $((MAX_RETRIES * 3)) seconds."
    echo "  Check 'docker compose logs kestra' for details."
    exit 1
fi

echo ""
echo "============================================="
echo "  Kestra UI: http://localhost:8080"
echo "  Login:     ${KESTRA_ADMIN_USERNAME:-admin@kestra.io} / ${KESTRA_ADMIN_PASSWORD:-Admin1234!}"
echo "============================================="
echo ""

# -- Step 6: Import flows via Kestra API -----------------------------------
echo "Importing flows..."
for flow in flows/*.yaml; do
    fname=$(basename "$flow")
    echo "  Importing $fname..."
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
        -X POST \
        -u "${KESTRA_ADMIN_USERNAME:-admin@kestra.io}:${KESTRA_ADMIN_PASSWORD:-Admin1234!}" \
        "http://localhost:8080/api/v1/flows/import" \
        -F "fileUpload=@$flow" 2>/dev/null || echo "000")
    if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "204" ]; then
        echo "    OK $fname imported"
    else
        echo "    WARN $fname returned HTTP $HTTP_CODE (may already exist)"
    fi
done

echo ""
echo "OK Setup complete!"
echo "  Open http://localhost:8080 to view your flows."

# Remove the trap on success
trap - EXIT
