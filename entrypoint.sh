#!/bin/sh
exec python /odoo/odoo-bin \
    --db_host="$DB_HOST" \
    --db_port="$DB_PORT" \
    --db_user="$DB_USER" \
    --db_password="$DB_PASSWORD" \
    --database="$DB_NAME" \
    --addons-path=/odoo/addons,/mnt/extra-addons \
    --http-port="${PORT:-8069}" \
    -i base \
    --without-demo=all
