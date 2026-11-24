def migrate(cr, version):
    cr.execute("""
        UPDATE res_users u
        SET active = FALSE
        WHERE u.id IN (
            SELECT p.user_id FROM op_parent p
            WHERE p.active = FALSE AND p.user_id IS NOT NULL
        )
    """)
    cr.execute("""
        DELETE FROM res_user_first_rel1
        WHERE user_id IN (
            SELECT p.user_id FROM op_parent p
            WHERE p.active = FALSE AND p.user_id IS NOT NULL
        )
    """)
