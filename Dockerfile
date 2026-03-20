FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libxml2-dev libxslt1-dev libldap2-dev libsasl2-dev \
    libpq-dev git curl node-less npm \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/odoo/odoo --depth 1 --branch 17.0 /odoo

WORKDIR /odoo
RUN pip install -r requirements.txt && pip install phonenumbers "setuptools<71"

COPY . /mnt/extra-addons

EXPOSE 8069

CMD python odoo-bin \
    --db_host=$DB_HOST \
    --db_port=$DB_PORT \
    --db_user=$DB_USER \
    --db_password=$DB_PASSWORD \
    --database=$DB_NAME \
    --addons-path=/odoo/addons,/mnt/extra-addons \
    --http-port=8069 \
    -i base \
    --without-demo=all
