# openEMIS – Custom Odoo Image
# Extends the official Odoo 17.0 image with openEMIS modules pre-installed.
#
# Build:
#   docker build -t openemis:latest .
#
# Run (standalone, requires a running PostgreSQL instance):
#   docker run -p 8069:8069 --env HOST=<pg-host> --env USER=odoo \
#     --env PASSWORD=odoo openemis:latest

FROM odoo:18.0

LABEL maintainer="openEMIS <support@openemis.org>" \
      org.opencontainers.image.title="openEMIS" \
      org.opencontainers.image.description="Open Source Educational Management Information System" \
      org.opencontainers.image.url="https://www.openemis.org" \
      org.opencontainers.image.source="https://github.com/eodenyire/openEMIS" \
      org.opencontainers.image.licenses="LGPL-3.0"

USER root

# Copy all openEMIS addon modules into the extra-addons path
COPY --chown=odoo:odoo . /mnt/extra-addons/

# Install any additional Python dependencies needed by openEMIS modules
RUN pip3 install --no-cache-dir requests

USER odoo

# Default command: start Odoo with openEMIS addons path
CMD ["odoo", \
     "--addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons"]
