from odoo import models, api


def post_init_hook(env):
    _rename_openeducat(env)


def _rename_openeducat(env):
    # Renommer TOUS les modules openeducat (installés ou non)
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
        nouveau = renommages.get(d.name)
        if nouveau:
            menu.name = nouveau


class IrModuleModule(models.Model):
    _inherit = 'ir.module.module'

    def button_immediate_install(self):
        result = super().button_immediate_install()
        if any('openeducat' in m.name for m in self):
            _rename_openeducat(self.env)
        return result
