FROM gitpod/workspace-postgres

USER root
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    libxml2-dev libxslt1-dev libldap2-dev libsasl2-dev \
    libpq-dev git curl node-less npm \
    && rm -rf /var/lib/apt/lists/*

USER gitpod
