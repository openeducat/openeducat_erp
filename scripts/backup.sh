#!/bin/bash
mkdir -p /workspaces/soome_erp/backups
for db in $(psql -U postgres -h 127.0.0.1 -t -c "SELECT datname FROM pg_database WHERE datistemplate=false AND datname NOT IN ('postgres');" 2>/dev/null); do
    db=$(echo $db | tr -d ' ')
    if [ -n "$db" ]; then
        echo "Sauvegarde de $db..."
        pg_dump -U odoo -h 127.0.0.1 "$db" > /workspaces/soome_erp/backups/${db}.sql
        echo "✅ $db sauvegardé"
    fi
done
