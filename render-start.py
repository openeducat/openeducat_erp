#!/usr/bin/env python3
"""Render entrypoint for OpenEduCat with Supabase and Backblaze B2."""
import configparser
import io
import json
import os
import re
import subprocess
import sys
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
config_text = io.StringIO()
server_config.write(config_text)
os.environ["SERVER_ENV_CONFIG"] = config_text.getvalue()
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

port = os.environ.get("PORT", "10000")
common = [
    "odoo",
    "--database", db_name,
    "--db-filter", "^" + re.escape(db_name) + "$",
    "--http-interface", "0.0.0.0",
    "--http-port", port,
    "--proxy-mode",
    "--without-demo=all",
    "--max-cron-threads=1",
    "--log-level=info",
]

# Install the OpenEduCat ERP bundle and the B2 attachment backend on first
# boot. Odoo leaves already-installed modules alone on later starts.
init_command = common + [
    "--init", "openeducat_erp,tl_b2_attachment_storage",
    "--stop-after-init",
]
subprocess.run(init_command, check=True, env=os.environ.copy())

os.execvp(common[0], common)
