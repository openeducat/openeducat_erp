#!/bin/sh
exec python /odoo/odoo-bin \
    --db_host="$PGHOST" \
    --db_port="$PGPORT" \
    --db_user="$PGUSER" \
    --db_password="$PGPASSWORD" \
    --addons-path=/odoo/addons,/mnt/extra-addons \
    --http-port="${PORT:-8069}" \
    --without-demo=all \
    --load=base,web
