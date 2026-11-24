def migrate(cr, version):
    cr.execute("""
        UPDATE ir_model_access
        SET perm_write = FALSE,
            perm_create = FALSE,
            perm_unlink = FALSE
        WHERE name = 'name_res_users_back_office_admin'
    """)
