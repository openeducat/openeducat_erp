# Gap 12: Parent Manager previously had full CRUD on res.users (operation='crud').
# Downgrade existing installs to read-only so a parent manager can no longer
# write / create / delete arbitrary users (incl. admin).


def migrate(cr, version):
    cr.execute("""
        UPDATE ir_access
        SET operation = 'r'
        WHERE name = 'name_res_users_back_office_admin'
          AND operation = 'crud'
    """)
