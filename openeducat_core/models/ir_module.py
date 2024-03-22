# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.osv.expression import is_leaf
from odoo.exceptions import AccessDenied, UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)


class IrModule(models.Model):
    _inherit = "ir.module.module"

    module_type = fields.Selection(selection_add=[('institutes', 'Institutes')])

    @api.model
    def _get_modules_from_apps(self, fields, module_type, module_name, domain=None, limit=None, offset=None):
        print(module_type, '.module_type')
        if module_type == 'institutes':
            module_lst = []
            all_module_lst = []
            institutes_categories = self._get_institutes_categories_from_apps()
            for data in institutes_categories:
                all_mod = self.env['ir.module.module'].search([('category_id.name', 'ilike', data)])
                for modules in all_mod:
                    module_lst.append(modules)
            for module in module_lst:
                values = {}
                values.update({
                    'id': module.id,
                    'summary': module.summary,
                    'name': module.name,
                    'icon': module.icon,
                    'shortdesc': module.shortdesc,
                    'website': module.website,
                    'application': module.application,
                    'module_type': 'institutes'
                })
                all_module_lst.append(values)
            modules_list = all_module_lst
            for mod in modules_list:
                module_name = mod['name']
                existing_mod = self.search([('name', '=', module_name), ('state', '=', 'installed')])
                if 'state' in fields:
                    if existing_mod:
                        mod['state'] = 'installed'
                    else:
                        mod['state'] = 'uninstalled'
                if 'module_type' in fields:
                    mod['module_type'] = module_type
            return modules_list
        return super()._get_modules_from_apps(fields, module_type, module_name, domain, limit, offset)

    @api.model
    def web_search_read(self, domain, specification, offset=0, limit=None, order=None, count_limit=None):
        res = super(IrModule, self).web_search_read(domain, specification, offset=offset, limit=limit, order=order,
                                                    count_limit=count_limit)
        if _domain_asks_for_institutes(domain):
            fields_name = list(specification.keys())
            modules_list = self._get_modules_from_apps(fields_name, 'institutes', False, domain, offset=offset,
                                                       limit=limit)
            return {
                'length': len(modules_list),
                'records': modules_list,
            }
        else:
            return res

    @api.model
    def _get_institutes_categories_from_apps(self):
        lst = ['institutes']
        return lst

    @api.model
    def search_panel_select_range(self, field_name, **kwargs):
        res = super(IrModule, self).search_panel_select_range(field_name, **kwargs)
        if field_name == 'category_id' and _domain_asks_for_institutes(kwargs.get('category_domain', [])):
            categories = self._get_institutes_categories_from_apps()
            return {
                'parent_field': 'parent_id',
                'values': categories,
            }
        return res


def _domain_asks_for_institutes(domain):
    for dom in domain:
        if is_leaf(dom) and dom[0] == 'module_type':
            if dom[2] == 'institutes':
                if dom[1] != '=':
                    raise UserError('%r is an unsupported leaf' % (dom,))
                return True
    return False
