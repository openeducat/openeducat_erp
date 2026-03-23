#!/bin/bash
for sqlfile in /workspaces/soome_erp/backups/*.sql; do
    [ -f "$sqlfile" ] || continue
    db=$(basename "$sqlfile" .sql)
    echo "Restauration de $db..."
    psql -U postgres -h 127.0.0.1 -c "CREATE DATABASE \"$db\" OWNER odoo;" 2>/dev/null || true
    psql -U odoo -h 127.0.0.1 "$db" < "$sqlfile"
    echo "✅ $db restauré"
done
