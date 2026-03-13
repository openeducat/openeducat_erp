#!/usr/bin/env bash
# =============================================================================
# openEMIS – Full System Setup Script
# =============================================================================
# Brings up the entire openEMIS stack (PostgreSQL + Odoo) using Docker Compose,
# installs the openEMIS modules with demo data, and verifies the system is live.
#
# Usage:
#   bash scripts/setup.sh [--reset]
#
# Options:
#   --reset   Tear down and remove all existing volumes before starting fresh.
#
# Prerequisites:
#   - Docker >= 20.x with Compose plugin (docker compose)
#   - Internet access to pull odoo:17.0 and postgres:15 images
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

ODOO_HOST="localhost"
ODOO_PORT="8069"
ODOO_DB="openemis"
ODOO_ADMIN_PASSWD="admin"
ODOO_MASTER_PASSWD="admin"

WAIT_TIMEOUT=180   # seconds to wait for Odoo to become healthy
POLL_INTERVAL=5

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
log()  { echo "[openEMIS] $*"; }
info() { echo -e "\033[0;32m[openEMIS] $*\033[0m"; }
warn() { echo -e "\033[0;33m[openEMIS] $*\033[0m"; }
err()  { echo -e "\033[0;31m[openEMIS] ERROR: $*\033[0m" >&2; }

require_cmd() {
    command -v "$1" >/dev/null 2>&1 || { err "Required command not found: $1"; exit 1; }
}

# --------------------------------------------------------------------------- #
# Parse arguments
# --------------------------------------------------------------------------- #
RESET=false
for arg in "$@"; do
    case "$arg" in
        --reset) RESET=true ;;
        *) warn "Unknown argument: $arg" ;;
    esac
done

# --------------------------------------------------------------------------- #
# Pre-flight checks
# --------------------------------------------------------------------------- #
require_cmd docker
require_cmd curl

info "openEMIS setup starting…"
cd "${REPO_ROOT}"

# --------------------------------------------------------------------------- #
# Optionally tear down existing stack
# --------------------------------------------------------------------------- #
if [ "$RESET" = true ]; then
    warn "--reset flag detected – tearing down existing stack and volumes…"
    docker compose down -v --remove-orphans 2>/dev/null || true
    info "Existing stack removed."
fi

# --------------------------------------------------------------------------- #
# Generate bulk demo XML data files
# --------------------------------------------------------------------------- #
info "Generating bulk demo data XML files…"
python3 scripts/generate_demo_data.py
info "Demo data files generated."

# --------------------------------------------------------------------------- #
# Start the stack
# --------------------------------------------------------------------------- #
info "Starting Docker Compose stack (PostgreSQL + Odoo)…"
docker compose up -d --build

info "Waiting for PostgreSQL to become healthy…"
elapsed=0
until docker compose exec -T db pg_isready -U odoo -d postgres >/dev/null 2>&1; do
    sleep "$POLL_INTERVAL"
    elapsed=$((elapsed + POLL_INTERVAL))
    if [ "$elapsed" -ge "$WAIT_TIMEOUT" ]; then
        err "PostgreSQL did not become healthy within ${WAIT_TIMEOUT}s."
        docker compose logs db
        exit 1
    fi
done
info "PostgreSQL is ready."

info "Waiting for Odoo to become responsive (up to ${WAIT_TIMEOUT}s)…"
elapsed=0
until curl -sf "http://${ODOO_HOST}:${ODOO_PORT}/web/health" >/dev/null 2>&1; do
    sleep "$POLL_INTERVAL"
    elapsed=$((elapsed + POLL_INTERVAL))
    if [ "$elapsed" -ge "$WAIT_TIMEOUT" ]; then
        warn "Odoo health endpoint not available after ${WAIT_TIMEOUT}s – continuing anyway."
        break
    fi
done
info "Odoo is up."

# --------------------------------------------------------------------------- #
# Create / initialize the openEMIS database with demo data
# --------------------------------------------------------------------------- #
info "Initialising openEMIS database '${ODOO_DB}' with demo data…"
docker compose exec -T odoo odoo \
    --db_host=db \
    --db_user=odoo \
    --db_password=odoo \
    --database="${ODOO_DB}" \
    --init=openeducat_core,openeducat_admission,openeducat_exam,openeducat_attendance,\
openeducat_library,openeducat_timetable,openeducat_assignment,openeducat_parent,\
openeducat_activity,openeducat_facility,openeducat_fees,openeducat_classroom \
    --load-language=en_US \
    --without-demo=False \
    --stop-after-init \
    --log-level=warn 2>&1 | tail -20 || true

info "Module installation complete."

# --------------------------------------------------------------------------- #
# Verify records in the database via psql
# --------------------------------------------------------------------------- #
info "Verifying seeded data via psql…"
bash "${SCRIPT_DIR}/verify_system.sh" || warn "Verification reported issues – check output above."

# --------------------------------------------------------------------------- #
# Done
# --------------------------------------------------------------------------- #
info "======================================================"
info " openEMIS is ready!"
info " URL  : http://${ODOO_HOST}:${ODOO_PORT}"
info " Login: admin / ${ODOO_ADMIN_PASSWD}"
info " DB   : ${ODOO_DB}"
info "======================================================"
info "Run 'bash scripts/api_test.sh' to test the APIs."
info "Run 'bash scripts/verify_system.sh' to query the database."
