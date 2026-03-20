FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libxml2-dev libxslt1-dev libldap2-dev libsasl2-dev \
    libpq-dev git curl node-less npm \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/odoo/odoo --depth 1 --branch 17.0 /odoo

WORKDIR /odoo
RUN pip install -r requirements.txt && pip install phonenumbers "setuptools<71"

COPY . /mnt/extra-addons
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8069

ENTRYPOINT ["/entrypoint.sh"]
