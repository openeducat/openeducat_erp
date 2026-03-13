#!/usr/bin/env bash
# =============================================================================
# openEMIS – System Verification Script
# =============================================================================
# Verifies that the openEMIS system is running and the database contains the
# expected demo data.  Runs SQL queries against the PostgreSQL container and
# checks the Odoo health endpoint.
#
# Usage:
#   bash scripts/verify_system.sh [DB_HOST] [DB_PORT] [DB_NAME] [DB_USER] [DB_PASS]
#
# Defaults (Docker Compose environment):
#   DB_HOST = localhost
#   DB_PORT = 5432
#   DB_NAME = openemis
#   DB_USER = odoo
#   DB_PASS = odoo
# =============================================================================

set -euo pipefail

DB_HOST="${1:-localhost}"
DB_PORT="${2:-5432}"
DB_NAME="${3:-openemis}"
DB_USER="${4:-odoo}"
DB_PASS="${5:-odoo}"

ODOO_URL="${ODOO_URL:-http://localhost:8069}"

PASSED=0
FAILED=0

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
log()    { echo "[openEMIS verify] $*"; }
ok()     { echo -e "\033[0;32m  ✓ PASS\033[0m  $*"; PASSED=$((PASSED + 1)); }
fail()   { echo -e "\033[0;31m  ✗ FAIL\033[0m  $*"; FAILED=$((FAILED + 1)); }
header() { echo -e "\n\033[1;34m=== $* ===\033[0m"; }

export PGPASSWORD="${DB_PASS}"
PSQL="psql -h ${DB_HOST} -p ${DB_PORT} -U ${DB_USER} -d ${DB_NAME} -t -A"

# Check psql availability
if ! command -v psql >/dev/null 2>&1; then
    log "psql not found – using docker exec to run queries."
    PSQL="docker exec -i openemis_db psql -U ${DB_USER} -d ${DB_NAME} -t -A"
fi

run_sql() {
    # Run a SQL query and return the result
    echo "$1" | $PSQL 2>/dev/null || echo ""
}

# --------------------------------------------------------------------------- #
# 1. Odoo health check
# --------------------------------------------------------------------------- #
header "1. Odoo Health Check"
if command -v curl >/dev/null 2>&1; then
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "${ODOO_URL}/web/health" 2>/dev/null || echo "000")
    if [ "$HTTP_CODE" = "200" ]; then
        ok "Odoo health endpoint returned HTTP 200"
    else
        fail "Odoo health endpoint returned HTTP ${HTTP_CODE} (expected 200)"
    fi
else
    log "curl not available – skipping HTTP health check."
fi

# --------------------------------------------------------------------------- #
# 2. PostgreSQL connectivity
# --------------------------------------------------------------------------- #
header "2. PostgreSQL Connectivity"
DB_VERSION=$(run_sql "SELECT version();" | head -1)
if [ -n "$DB_VERSION" ]; then
    ok "PostgreSQL is accessible: ${DB_VERSION}"
else
    fail "Cannot connect to PostgreSQL at ${DB_HOST}:${DB_PORT}/${DB_NAME}"
    echo ""
    echo "Results: ${PASSED} passed, ${FAILED} failed."
    exit 1
fi

# --------------------------------------------------------------------------- #
# 3. Installed modules
# --------------------------------------------------------------------------- #
header "3. Installed openEMIS Modules"
MODULE_COUNT=$(run_sql "SELECT COUNT(*) FROM ir_module_module WHERE name LIKE 'openeducat%' AND state = 'installed';" | head -1)
if [ "${MODULE_COUNT:-0}" -gt 0 ] 2>/dev/null; then
    ok "${MODULE_COUNT} openEMIS module(s) installed"
    run_sql "SELECT name FROM ir_module_module WHERE name LIKE 'openeducat%' AND state = 'installed' ORDER BY name;" | \
        while read -r mod; do echo "   - ${mod}"; done
else
    fail "No openEMIS modules found as installed (count=${MODULE_COUNT:-?})"
fi

# --------------------------------------------------------------------------- #
# 4. Student records
# --------------------------------------------------------------------------- #
header "4. Student Records"
STU_COUNT=$(run_sql "SELECT COUNT(*) FROM op_student WHERE active = true;" | head -1)
if [ "${STU_COUNT:-0}" -ge 10 ] 2>/dev/null; then
    ok "Students in database: ${STU_COUNT}"
elif [ "${STU_COUNT:-0}" -gt 0 ] 2>/dev/null; then
    ok "Students in database: ${STU_COUNT} (fewer than expected – may need demo data reload)"
else
    fail "No students found in database (count=${STU_COUNT:-?})"
fi

# --------------------------------------------------------------------------- #
# 5. Faculty records
# --------------------------------------------------------------------------- #
header "5. Faculty Records"
FAC_COUNT=$(run_sql "SELECT COUNT(*) FROM op_faculty WHERE active = true;" | head -1)
if [ "${FAC_COUNT:-0}" -ge 5 ] 2>/dev/null; then
    ok "Faculty in database: ${FAC_COUNT}"
elif [ "${FAC_COUNT:-0}" -gt 0 ] 2>/dev/null; then
    ok "Faculty in database: ${FAC_COUNT} (fewer than expected)"
else
    fail "No faculty found in database (count=${FAC_COUNT:-?})"
fi

# --------------------------------------------------------------------------- #
# 6. Course records
# --------------------------------------------------------------------------- #
header "6. Course Records"
COURSE_COUNT=$(run_sql "SELECT COUNT(*) FROM op_course WHERE active = true;" | head -1)
if [ "${COURSE_COUNT:-0}" -ge 5 ] 2>/dev/null; then
    ok "Courses in database: ${COURSE_COUNT}"
else
    fail "Fewer than 5 courses found (count=${COURSE_COUNT:-?})"
fi

# --------------------------------------------------------------------------- #
# 7. Classroom records
# --------------------------------------------------------------------------- #
header "7. Classroom Records"
CLASS_COUNT=$(run_sql "SELECT COUNT(*) FROM op_classroom;" 2>/dev/null | head -1 || echo "0")
if [ "${CLASS_COUNT:-0}" -ge 1 ] 2>/dev/null; then
    ok "Classrooms in database: ${CLASS_COUNT}"
else
    fail "No classrooms found (count=${CLASS_COUNT:-?}). Run: python3 scripts/generate_demo_data.py"
fi

# --------------------------------------------------------------------------- #
# 8. Student–Course enrolments
# --------------------------------------------------------------------------- #
header "8. Student–Course Enrolments"
ENROL_COUNT=$(run_sql "SELECT COUNT(*) FROM op_student_course;" | head -1)
if [ "${ENROL_COUNT:-0}" -ge 5 ] 2>/dev/null; then
    ok "Student–course enrolments: ${ENROL_COUNT}"
else
    fail "Fewer than 5 enrolments found (count=${ENROL_COUNT:-?})"
fi

# --------------------------------------------------------------------------- #
# 9. Academic year / term
# --------------------------------------------------------------------------- #
header "9. Academic Year & Term"
YEAR_COUNT=$(run_sql "SELECT COUNT(*) FROM op_academic_year;" | head -1)
TERM_COUNT=$(run_sql "SELECT COUNT(*) FROM op_academic_term;" | head -1)
if [ "${YEAR_COUNT:-0}" -ge 1 ] 2>/dev/null; then
    ok "Academic years: ${YEAR_COUNT}"
else
    fail "No academic years found"
fi
if [ "${TERM_COUNT:-0}" -ge 1 ] 2>/dev/null; then
    ok "Academic terms: ${TERM_COUNT}"
else
    fail "No academic terms found"
fi

# --------------------------------------------------------------------------- #
# 10. Sample data printout
# --------------------------------------------------------------------------- #
header "10. Sample Data"
log "First 5 students:"
run_sql "SELECT first_name || ' ' || last_name AS name, gender, birth_date FROM op_student WHERE active=true ORDER BY last_name LIMIT 5;" | \
    while IFS='|' read -r name gender dob; do
        echo "   - ${name} (${gender}, born ${dob})"
    done

log "First 5 faculty:"
run_sql "SELECT first_name || ' ' || last_name AS name, gender FROM op_faculty WHERE active=true ORDER BY last_name LIMIT 5;" | \
    while IFS='|' read -r name gender; do
        echo "   - ${name} (${gender})"
    done

# --------------------------------------------------------------------------- #
# Summary
# --------------------------------------------------------------------------- #
echo ""
echo "======================================================"
if [ "$FAILED" -eq 0 ]; then
    echo -e "\033[0;32m  All ${PASSED} checks passed!\033[0m"
else
    echo -e "\033[0;31m  ${PASSED} passed, ${FAILED} FAILED.\033[0m"
fi
echo "======================================================"

[ "$FAILED" -eq 0 ] || exit 1
