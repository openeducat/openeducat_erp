#!/bin/sh
exec python /odoo/odoo-bin \
    --db_host="$PGHOST" \
    --db_port="$PGPORT" \
    --db_user="$PGUSER" \
    --db_password="$PGPASSWORD" \
    --database=railway \
    --db-filter="^railway$" \
    --addons-path=/odoo/addons,/mnt/extra-addons \
    --http-port="${PORT:-8069}" \
    --without-demo=all \
    -i base,web,mail,auth_totp,base_import,base_setup,bus,web_tour,iap,web_editor
