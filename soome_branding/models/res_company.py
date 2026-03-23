from odoo import api, SUPERUSER_ID


def post_init_hook(env):
    # Renommer les modules OpenEduCat -> SOOME
    modules = env['ir.module.module'].search([('name', 'like', 'openeducat')])
    for m in modules:
        if 'OpenEduCat' in (m.shortdesc or ''):
            m.shortdesc = m.shortdesc.replace('OpenEduCat', 'SOOME')

    # Renommer les menus racines
    renommages = {
        'menu_op_school_root': 'SOOME',
        'menu_op_faculty_root': 'SOOME - Enseignants',
        'menu_openeducat_config': 'SOOME - Paramètres',
    }
    data = env['ir.model.data'].search([
        ('module', 'like', 'openeducat'),
        ('model', '=', 'ir.ui.menu'),
        ('name', 'in', list(renommages.keys()))
    ])
    for d in data:
        menu = env['ir.ui.menu'].browse(d.res_id)
        nouveau_nom = renommages.get(d.name)
        if nouveau_nom:
            menu.name = nouveau_nom

    env.cr.commit()
