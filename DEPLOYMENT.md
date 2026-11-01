# TrueLearners OpenEduCat deployment

This branch contains a Docker deployment for the OpenEduCat 19.0 source in this repository.

## Architecture

- Render Docker web service runs Odoo/OpenEduCat 19.0.
- Supabase PostgreSQL stores application data.
- Backblaze B2 (private S3-compatible bucket) stores attachment files through OCA's Odoo 19 storage addons.
- The Render service uses ephemeral local storage for temporary files and sessions only. OCA's attachment backend keeps normal uploaded attachments in B2; small images and web assets covered by the OCA default rules remain in PostgreSQL.

## Before deploying

1. Rotate the Supabase database password. A previous version of `render.yaml` committed a database credential. Removing it from the latest file does not remove it from Git history. Treat it as exposed.
2. In Supabase, use the **Session pooler** connection details, not the Transaction pooler. Use the host and username exactly as shown in Supabase. The database name is normally `postgres`; verify it in the Supabase dashboard.
3. Confirm the Supabase role can create tables, indexes, and the extensions required by Odoo in the selected database. Odoo initializes its schema in the existing database; this deployment does not create a new Supabase database.
4. Create a **private** Backblaze B2 bucket. Create an application key scoped only to that bucket, with the read/write/delete permissions needed by Odoo. Do not make the bucket public.
5. Record the bucket's S3 endpoint and region from Backblaze. The endpoint is usually of the form `https://s3.<region>.backblazeb2.com`. Use the exact values shown by Backblaze.
6. Review the Render compute plan and price with the account owner before creating a paid service. The blueprint uses `2c-4g` (2 CPUs, 4 GB RAM); Render's free plan is too small for this deployment.

## Render environment variables

Set these as secrets in Render. Do not commit their values.

| Key | Value |
| --- | --- |
| `HOST` | Supabase Session Pooler hostname |
| `USER` | Supabase Session Pooler username |
| `PASSWORD` | Newly rotated Supabase database password |
| `PGPORT` | `5432` for the Session Pooler |
| `PGSSLMODE` | `require` |
| `DB_NAME` | Existing Supabase database name, usually `postgres` |
| `B2_ENDPOINT_URL` | Backblaze S3 endpoint for the bucket's region |
| `B2_REGION` | Backblaze region identifier |
| `B2_BUCKET` | Exact private bucket name |
| `B2_ACCESS_KEY_ID` | Bucket-scoped Backblaze application key ID |
| `B2_SECRET_ACCESS_KEY` | Matching Backblaze application key secret |

The startup script builds the OCA server-environment configuration in memory from these environment variables. It does not write the secrets into the Git repository.

## Deploy

1. In Render, create a Blueprint from this repository and select branch `deploy/render-supabase-b2`.
2. Review the proposed service and its paid compute plan before approving creation.
3. Add the environment variables above.
4. Set the custom domain to `edu.truelearners.org` after the first successful deployment, then add the DNS record Render displays.
5. Wait for the first startup to complete. It checks Supabase connectivity, installs `openeducat_erp` and the B2 storage addon, and then starts Odoo.

## Important checks before real student data

- Verify the Odoo logs show a successful Supabase connection and module installation.
- In Odoo, confirm the storage record named **TrueLearners Backblaze B2** is present and is the default attachment storage.
- Upload, download, replace, and delete test files using a test account.
- Restart and redeploy the Render service, then verify those files still work.
- Check the private B2 bucket to confirm uploaded files are stored there.
- Confirm that deleting an Odoo attachment removes its external object as expected.
- Test a database backup and a separate B2 bucket backup/restore process. A database backup alone does not back up the B2 objects.
- Do not use real student records until these checks pass.

## Notes and limitations

- Supabase is being used as an existing Odoo database, not as a replacement for a full self-managed PostgreSQL server. Compatibility of Odoo's initialization, permissions, and required extensions must be confirmed by the first test deployment.
- OCA's S3 attachment addons on branch 19.0 are marked Beta. Test their upload/download/delete behavior before production.
- This deployment intentionally does not enable Odoo's database manager for creating arbitrary databases.
- The existing Moodle and WordPress services are not changed by this deployment.
