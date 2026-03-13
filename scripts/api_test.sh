#!/usr/bin/env bash
# =============================================================================
# openEMIS – Odoo JSON-RPC / XMLRPC API Test Script
# =============================================================================
# Exercises the major openEMIS API endpoints using curl (JSON-RPC over HTTP).
# Tests:
#   1. Server version check
#   2. Database list
#   3. Authentication (admin login)
#   4. Student record count
#   5. Faculty record count
#   6. Course listing (first 5)
#   7. Student search with filter
#   8. Create a student via API
#   9. Read back the created student
#  10. Delete the test student (cleanup)
#
# Usage:
#   bash scripts/api_test.sh [HOST] [PORT] [DB] [USER] [PASSWORD]
#
# Defaults:
#   HOST     = localhost
#   PORT     = 8069
#   DB       = openemis
#   USER     = admin
#   PASSWORD = admin
# =============================================================================

set -euo pipefail

HOST="${1:-localhost}"
PORT="${2:-8069}"
DB="${3:-openemis}"
USER="${4:-admin}"
PASSWORD="${5:-admin}"

BASE_URL="http://${HOST}:${PORT}"
JSONRPC="${BASE_URL}/web/dataset/call_kw"
PASSED=0
FAILED=0

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
log()    { echo "[openEMIS API] $*"; }
ok()     { echo -e "\033[0;32m  ✓ PASS\033[0m  $*"; PASSED=$((PASSED + 1)); }
fail()   { echo -e "\033[0;31m  ✗ FAIL\033[0m  $*"; FAILED=$((FAILED + 1)); }
header() { echo -e "\n\033[1;34m=== $* ===\033[0m"; }

# JSON-RPC helper – prints the result field of the response
jsonrpc() {
    local endpoint="$1"
    local payload="$2"
    curl -s -X POST \
        -H "Content-Type: application/json" \
        --cookie-jar /tmp/openemis_cookies.txt \
        --cookie /tmp/openemis_cookies.txt \
        "${BASE_URL}${endpoint}" \
        -d "${payload}"
}

# --------------------------------------------------------------------------- #
# 1. Server version
# --------------------------------------------------------------------------- #
header "1. Server Version"
VERSION_RESP=$(jsonrpc "/web/webclient/version_info" '{"jsonrpc":"2.0","method":"call","params":{}}')
SERVER_VERSION=$(echo "$VERSION_RESP" | python3 -c "import sys,json; r=json.load(sys.stdin); print(r.get('result',{}).get('server_version','?'))" 2>/dev/null || echo "?")
if [ "$SERVER_VERSION" != "?" ]; then
    ok "Server version: ${SERVER_VERSION}"
else
    fail "Could not read server version. Response: ${VERSION_RESP}"
fi

# --------------------------------------------------------------------------- #
# 2. Database list
# --------------------------------------------------------------------------- #
header "2. Database List"
DB_LIST_RESP=$(jsonrpc "/web/database/list" '{"jsonrpc":"2.0","method":"call","params":{}}')
if echo "$DB_LIST_RESP" | grep -q '"result"'; then
    ok "Database list endpoint is responsive"
else
    fail "Database list not readable. Response: ${DB_LIST_RESP}"
fi

# --------------------------------------------------------------------------- #
# 3. Authenticate
# --------------------------------------------------------------------------- #
header "3. Authentication"
AUTH_PAYLOAD=$(cat <<EOF
{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "db": "${DB}",
        "login": "${USER}",
        "password": "${PASSWORD}"
    }
}
EOF
)
AUTH_RESP=$(jsonrpc "/web/session/authenticate" "${AUTH_PAYLOAD}")
ODOO_UID=$(echo "$AUTH_RESP" | python3 -c "import sys,json; r=json.load(sys.stdin); print(r.get('result',{}).get('uid',''))" 2>/dev/null || echo "")
SESSION_ID=$(echo "$AUTH_RESP" | python3 -c "import sys,json; r=json.load(sys.stdin); print(r.get('result',{}).get('session_id',''))" 2>/dev/null || echo "")

if [ -n "$ODOO_UID" ] && [ "$ODOO_UID" != "None" ] && [ "$ODOO_UID" != "null" ]; then
    ok "Authenticated as '${USER}' (uid=${ODOO_UID})"
else
    fail "Authentication failed for user '${USER}'. Response: ${AUTH_RESP}"
    log "Skipping authenticated tests."
    echo ""
    echo "Results: ${PASSED} passed, ${FAILED} failed."
    exit 1
fi

# Helper for authenticated RPC calls
rpc_call() {
    local model="$1"
    local method="$2"
    local args="$3"
    local kwargs
    kwargs="${4-}"
    if [ -z "$kwargs" ]; then kwargs="{}"; fi
    local payload
    payload=$(cat <<EOF
{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "model": "${model}",
        "method": "${method}",
        "args": ${args},
        "kwargs": ${kwargs}
    }
}
EOF
)
    jsonrpc "/web/dataset/call_kw" "${payload}"
}

# --------------------------------------------------------------------------- #
# 4. Student count
# --------------------------------------------------------------------------- #
header "4. Student Count"
STU_RESP=$(rpc_call "op.student" "search_count" '[[["active","=",true]]]')
STU_COUNT=$(echo "$STU_RESP" | python3 -c "import sys,json; r=json.load(sys.stdin); print(r.get('result','?'))" 2>/dev/null || echo "?")
if [ "$STU_COUNT" != "?" ] && [ "$STU_COUNT" != "null" ]; then
    ok "Active students in database: ${STU_COUNT}"
else
    fail "Could not retrieve student count. Response: ${STU_RESP}"
fi

# --------------------------------------------------------------------------- #
# 5. Faculty count
# --------------------------------------------------------------------------- #
header "5. Faculty Count"
FAC_RESP=$(rpc_call "op.faculty" "search_count" '[[["active","=",true]]]')
FAC_COUNT=$(echo "$FAC_RESP" | python3 -c "import sys,json; r=json.load(sys.stdin); print(r.get('result','?'))" 2>/dev/null || echo "?")
if [ "$FAC_COUNT" != "?" ] && [ "$FAC_COUNT" != "null" ]; then
    ok "Active faculty in database: ${FAC_COUNT}"
else
    fail "Could not retrieve faculty count. Response: ${FAC_RESP}"
fi

# --------------------------------------------------------------------------- #
# 6. Course listing (first 5)
# --------------------------------------------------------------------------- #
header "6. Course Listing (first 5)"
COURSE_RESP=$(rpc_call "op.course" "search_read" \
    '[[["active","=",true]]]' \
    '{"fields":["name","code"],"limit":5}')
COURSE_COUNT=$(echo "$COURSE_RESP" | python3 -c \
    "import sys,json; r=json.load(sys.stdin); print(len(r.get('result',[])))" 2>/dev/null || echo "0")
if [ "$COURSE_COUNT" -gt 0 ] 2>/dev/null; then
    ok "Courses retrieved: ${COURSE_COUNT}"
    echo "$COURSE_RESP" | python3 -c \
        "import sys,json; [print('   -', c['name']) for c in json.load(sys.stdin).get('result',[])]" 2>/dev/null || true
else
    fail "No courses found. Response: ${COURSE_RESP}"
fi

# --------------------------------------------------------------------------- #
# 7. Student search with filter
# --------------------------------------------------------------------------- #
header "7. Student Search (gender=female, limit 3)"
FILTER_RESP=$(rpc_call "op.student" "search_read" \
    '[[["gender","=","f"],["active","=",true]]]' \
    '{"fields":["first_name","last_name","gender"],"limit":3}')
FILTER_COUNT=$(echo "$FILTER_RESP" | python3 -c \
    "import sys,json; print(len(json.load(sys.stdin).get('result',[])))" 2>/dev/null || echo "0")
if [ "$FILTER_COUNT" -gt 0 ] 2>/dev/null; then
    ok "Female students returned: ${FILTER_COUNT}"
    echo "$FILTER_RESP" | python3 -c \
        "import sys,json; [print('   -', s['first_name'], s['last_name']) for s in json.load(sys.stdin).get('result',[])]" 2>/dev/null || true
else
    fail "No female students found. Response: ${FILTER_RESP}"
fi

# --------------------------------------------------------------------------- #
# 8. Create a student via API
# --------------------------------------------------------------------------- #
header "8. Create Test Student via API"

# First create a partner
PARTNER_PAYLOAD=$(cat <<EOF
{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "model": "res.partner",
        "method": "create",
        "args": [{"name": "API Test Student openEMIS", "email": "api_test_student@openemis.example.com"}],
        "kwargs": {}
    }
}
EOF
)
PARTNER_RESP=$(jsonrpc "/web/dataset/call_kw" "${PARTNER_PAYLOAD}")
PARTNER_ID=$(echo "$PARTNER_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('result',''))" 2>/dev/null || echo "")

if [ -n "$PARTNER_ID" ] && [ "$PARTNER_ID" != "None" ]; then
    ok "Test partner created (id=${PARTNER_ID})"

    # Now create the student
    STU_CREATE_PAYLOAD=$(cat <<EOF
{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "model": "op.student",
        "method": "create",
        "args": [{
            "first_name": "APITest",
            "last_name": "Student",
            "birth_date": "2005-03-15",
            "gender": "m",
            "partner_id": ${PARTNER_ID}
        }],
        "kwargs": {}
    }
}
EOF
)
    STU_CREATE_RESP=$(jsonrpc "/web/dataset/call_kw" "${STU_CREATE_PAYLOAD}")
    NEW_STU_ID=$(echo "$STU_CREATE_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('result',''))" 2>/dev/null || echo "")

    if [ -n "$NEW_STU_ID" ] && [ "$NEW_STU_ID" != "None" ]; then
        ok "Test student created (id=${NEW_STU_ID})"
    else
        fail "Student creation failed. Response: ${STU_CREATE_RESP}"
        NEW_STU_ID=""
    fi
else
    fail "Partner creation failed. Response: ${PARTNER_RESP}"
    PARTNER_ID=""
    NEW_STU_ID=""
fi

# --------------------------------------------------------------------------- #
# 9. Read back the created student
# --------------------------------------------------------------------------- #
header "9. Read Back Created Student"
if [ -n "$NEW_STU_ID" ]; then
    READ_PAYLOAD=$(cat <<EOF
{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "model": "op.student",
        "method": "read",
        "args": [[${NEW_STU_ID}]],
        "kwargs": {"fields": ["first_name","last_name","gender","birth_date"]}
    }
}
EOF
)
    READ_RESP=$(jsonrpc "/web/dataset/call_kw" "${READ_PAYLOAD}")
    READ_NAME=$(echo "$READ_RESP" | python3 -c \
        "import sys,json; r=json.load(sys.stdin)['result']; print(r[0]['first_name'] + ' ' + r[0]['last_name'])" 2>/dev/null || echo "")
    if [ "$READ_NAME" = "APITest Student" ]; then
        ok "Read back student: ${READ_NAME}"
    else
        fail "Unexpected student data. Response: ${READ_RESP}"
    fi
else
    log "Skipping read-back (student not created)."
fi

# --------------------------------------------------------------------------- #
# 10. Delete test student (cleanup)
# --------------------------------------------------------------------------- #
header "10. Cleanup – Delete Test Student"
if [ -n "$NEW_STU_ID" ]; then
    DEL_PAYLOAD=$(cat <<EOF
{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "model": "op.student",
        "method": "unlink",
        "args": [[${NEW_STU_ID}]],
        "kwargs": {}
    }
}
EOF
)
    DEL_RESP=$(jsonrpc "/web/dataset/call_kw" "${DEL_PAYLOAD}")
    DEL_RESULT=$(echo "$DEL_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('result',''))" 2>/dev/null || echo "")
    if [ "$DEL_RESULT" = "True" ] || [ "$DEL_RESULT" = "true" ]; then
        ok "Test student deleted successfully"
    else
        fail "Student deletion returned unexpected result. Response: ${DEL_RESP}"
    fi
fi

# Cleanup test partner
if [ -n "$PARTNER_ID" ]; then
    DEL_P_PAYLOAD=$(cat <<EOF
{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "model": "res.partner",
        "method": "unlink",
        "args": [[${PARTNER_ID}]],
        "kwargs": {}
    }
}
EOF
)
    jsonrpc "/web/dataset/call_kw" "${DEL_P_PAYLOAD}" >/dev/null 2>&1 || true
fi

# --------------------------------------------------------------------------- #
# Summary
# --------------------------------------------------------------------------- #
echo ""
echo "======================================================"
if [ "$FAILED" -eq 0 ]; then
    echo -e "\033[0;32m  All ${PASSED} API tests passed!\033[0m"
else
    echo -e "\033[0;31m  ${PASSED} passed, ${FAILED} FAILED.\033[0m"
fi
echo "======================================================"

rm -f /tmp/openemis_cookies.txt
[ "$FAILED" -eq 0 ] || exit 1
