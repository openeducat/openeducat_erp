#!/usr/bin/env python3
"""Render entrypoint for OpenEduCat with Supabase and Backblaze B2."""
import configparser
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import time

required = [
    "HOST", "USER", "PASSWORD", "DB_NAME",
    "B2_ENDPOINT_URL", "B2_REGION", "B2_BUCKET",
    "B2_ACCESS_KEY_ID", "B2_SECRET_ACCESS_KEY",
]
missing = [key for key in required if not os.environ.get(key)]
if missing:
    print("Missing required Render environment variables: " + ", ".join(missing), flush=True)
    sys.exit(1)

# OCA/server-env reads this before Odoo loads the addon registry. Credentials
# stay in Render's environment and are never committed to this repository.
server_config = configparser.ConfigParser(interpolation=None)
server_config.optionxform = str
server_config["fs_storage.b2"] = {
    "protocol": "s3",
    "options": json.dumps({
        "endpoint_url": os.environ["B2_ENDPOINT_URL"],
        "key": os.environ["B2_ACCESS_KEY_ID"],
        "secret": os.environ["B2_SECRET_ACCESS_KEY"],
        "client_kwargs": {"region_name": os.environ["B2_REGION"]},
    }),
    "directory_path": os.environ["B2_BUCKET"],
    "eval_options_from_env": "false",
    "use_as_default_for_attachments": "true",
    "autovacuum_gc": "true",
    "force_db_for_default_attachment_rules": json.dumps({
        "image/": 51200,
        "application/javascript": 0,
        "text/css": 0,
    }),
}
server_text = io.StringIO()
server_config.write(server_text)
os.environ["SERVER_ENV_CONFIG"] = server_text.getvalue()
os.environ["PGSSLMODE"] = "require"

db_name = os.environ["DB_NAME"]
db_host = os.environ["HOST"]
db_port = int(os.environ.get("PGPORT", "5432"))
db_user = os.environ["USER"]
db_password = os.environ["PASSWORD"]

# Fail clearly if Supabase is unreachable before starting Odoo's module setup.
import psycopg2

for attempt in range(1, 31):
    try:
        connection = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password,
            sslmode="require",
            connect_timeout=10,
        )
        connection.close()
        break
    except Exception as exc:
        if attempt == 30:
            print("Could not connect to Supabase after 30 attempts: " + str(exc), flush=True)
            sys.exit(1)
        print(f"Waiting for Supabase connection ({attempt}/30)...", flush=True)
        time.sleep(5)

# Write the Odoo database credentials to a private, temporary config file.
# This avoids putting the password in command-line arguments or Git.
port = os.environ.get("PORT", "10000")
odoo_config = configparser.ConfigParser(interpolation=None)
odoo_config["options"] = {
    "db_host": db_host,
    "db_port": str(db_port),
    "db_user": db_user,
    "db_password": db_password,
    "db_sslmode": "require",
    "db_name": db_name,
    "dbfilter": "^" + re.escape(db_name) + "$",
    "list_db": "False",
    "http_interface": "0.0.0.0",
    "http_port": port,
    "proxy_mode": "True",
    "without_demo": "all",
    "max_cron_threads": "1",
    "log_level": "info",
}
config_file = tempfile.NamedTemporaryFile(
    mode="w", prefix="odoo-render-", suffix=".conf", delete=False
)
try:
    os.chmod(config_file.name, 0o600)
    odoo_config.write(config_file)
    config_file.close()
except Exception:
    config_file.close()
    raise

os.environ["ODOO_RC"] = config_file.name
common = ["odoo", "--config", config_file.name]

# Install the OpenEduCat ERP bundle and the B2 attachment backend on first
# boot. Odoo leaves already-installed modules alone on later starts.
subprocess.run(
    common + ["--init", "openeducat_erp,tl_b2_attachment_storage", "--stop-after-init"],
    check=True,
    env=os.environ.copy(),
)

os.execvp(common[0], common)
