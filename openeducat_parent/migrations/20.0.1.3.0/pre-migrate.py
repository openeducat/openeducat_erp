# Gap 13: op.parent gains company_id (multi-company isolation).
# Pre-create the column and backfill before the ORM loads the model, so the
# multi-company rule the module registers has a column to filter on.


def migrate(cr, version):
    cr.execute("""
        ALTER TABLE op_parent
        ADD COLUMN IF NOT EXISTS company_id integer
    """)
    cr.execute("""
        UPDATE op_parent
        SET company_id = (SELECT MIN(id) FROM res_company)
        WHERE company_id IS NULL
    """)
