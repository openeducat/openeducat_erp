# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from openerp import models, fields, api


class WizardOpStudent(models.TransientModel):
    _name = 'wizard.op.student'
    _description = "Create User the selected Students"

    def _get_students(self):
        if self.env.context and self.env.context.get('active_ids'):
            return self.env.context.get('active_ids')
        return []

    student_ids = fields.Many2many(
        'op.student', default=_get_students, string='Students')

    @api.one
    def create_user(self):
        student_pool = self.env['op.student']
        user_pool = self.env['res.users']
        user_fields = user_pool.fields_get(self)
        user_default = user_pool.default_get(user_fields)
        user_default_group_lst = user_default['groups_id']
        student_group_id = self.env.ref('openeducat_erp.group_op_student').id
        user_default_group_lst[0][2].append(student_group_id)
        user_default['groups_id'] = user_default_group_lst
        active_ids = self.env.context.get('active_ids', []) or []
        for stud in student_pool.browse(active_ids):
            if not stud.user_id:
                user_vals = {
                    'name': stud.name,
                    'login': stud.name,
                    'partner_id': stud.partner_id.id
                }
                user_default.update(user_vals)
                user_id = user_pool.create(user_default)
                stud.user_id = user_id


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
