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
