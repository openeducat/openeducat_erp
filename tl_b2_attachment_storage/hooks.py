import os


def post_init_hook(env):
    """Create the default B2 attachment storage record once."""
    bucket = os.environ.get("B2_BUCKET")
    if not bucket:
        raise RuntimeError("B2_BUCKET must be configured before installing this addon")

    storage_model = env["fs.storage"].sudo()
    storage = storage_model.search([("code", "=", "b2")], limit=1)
    values = {
        "name": "TrueLearners Backblaze B2",
        "code": "b2",
        "protocol": "s3",
        "options": "{}",
        "directory_path": bucket,
        "use_as_default_for_attachments": True,
        "autovacuum_gc": True,
        "force_db_for_default_attachment_rules": (
            '{"image/": 51200, "application/javascript": 0, "text/css": 0}'
        ),
    }
    if storage:
        storage.write(values)
    else:
        storage_model.create(values)
