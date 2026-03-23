from odoo import api, SUPERUSER_ID

def post_init_hook(env):
    menus = env['ir.ui.menu'].search([('name', 'like', 'OpenEduCat')])
    for menu in menus:
        menu.name = menu.name.replace('OpenEduCat', 'SOOME')
