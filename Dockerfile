FROM odoo:19.0

USER root

ARG OCA_STORAGE_REF=55f7de06ae47c7b8521cab2ed901853bd3ad259e
ARG OCA_SERVER_ENV_REF=00cd3d1aad34655c2a63b6f51a35dccaeddbd8b5

# Add the OCA storage and server-environment modules required for S3-compatible
# attachment storage. Pinning commits makes builds repeatable.
RUN apt-get update \
    && apt-get install -y --no-install-recommends git ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /tmp/oca-storage /tmp/oca-server-env /mnt/extra-addons \
    && git -C /tmp/oca-storage init \
    && git -C /tmp/oca-storage remote add origin https://github.com/OCA/storage.git \
    && git -C /tmp/oca-storage fetch --depth 1 origin "${OCA_STORAGE_REF}" \
    && git -C /tmp/oca-storage checkout --detach FETCH_HEAD \
    && git -C /tmp/oca-server-env init \
    && git -C /tmp/oca-server-env remote add origin https://github.com/OCA/server-env.git \
    && git -C /tmp/oca-server-env fetch --depth 1 origin "${OCA_SERVER_ENV_REF}" \
    && git -C /tmp/oca-server-env checkout --detach FETCH_HEAD \
    && for addon in fs_storage fs_storage_environment fs_attachment fs_attachment_environment fs_attachment_s3 fs_attachment_s3_environment; do \
         cp -a "/tmp/oca-storage/${addon}" /mnt/extra-addons/; \
       done \
    && cp -a /tmp/oca-server-env/server_environment /mnt/extra-addons/ \
    && rm -rf /tmp/oca-storage /tmp/oca-server-env

# fs_attachment_s3 uses fsspec's S3 backend (s3fs).
RUN python3 -m pip install --break-system-packages --no-cache-dir "fsspec[s3]>=2025.3.0"

# This repository contains the OpenEduCat 19.0 addon modules and the
# TrueLearners deployment addon. Keep addon folders at the top level.
COPY --chown=odoo:odoo . /mnt/extra-addons/

COPY --chown=root:root render-start.py /usr/local/bin/render-start.py
RUN chmod 755 /usr/local/bin/render-start.py

USER odoo

EXPOSE 10000

CMD ["python3", "/usr/local/bin/render-start.py"]
