#!/bin/sh
echo "PGHOST=$PGHOST"
echo "PGDATABASE=$PGDATABASE"
exec python /odoo/odoo-bin \
    --db_host="$PGHOST" \
    --db_port="$PGPORT" \
    --db_user="$PGUSER" \
    --db_password="$PGPASSWORD" \
    --database="$PGDATABASE" \
    --addons-path=/odoo/addons,/mnt/extra-addons \
    --http-port="${PORT:-8069}" \
    -i base \
    --without-demo=all
