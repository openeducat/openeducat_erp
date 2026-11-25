# Gap 14: op.parent.active cascades to res.users.active going forward. For
# installs that already have archived parents whose login is still active,
# archive the login and clear its child_ids so the attack surface closes
# on the first upgrade instead of only on the next archive event.


def migrate(cr, version):
    cr.execute("""
        UPDATE res_users u
        SET active = FALSE
        WHERE u.id IN (
            SELECT p.user_id
            FROM op_parent p
            WHERE p.active = FALSE AND p.user_id IS NOT NULL
        )
    """)
    cr.execute("""
        DELETE FROM res_user_first_rel1
        WHERE user_id IN (
            SELECT p.user_id
            FROM op_parent p
            WHERE p.active = FALSE AND p.user_id IS NOT NULL
        )
    """)
