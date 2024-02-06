# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<https://www.openeducat.org>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    signature = fields.Binary('Signature')
    accreditation = fields.Text('Accreditation')
    approval_authority = fields.Text('Approval Authority')


class ResUsers(models.Model):
    _inherit = "res.users"
    _parent_name = False

    def _department_count(self):
        return self.env['op.department'].sudo().search_count([])

    student_line = fields.Many2one('op.student', 'Line')
    user_line = fields.One2many('op.student', 'user_id', 'User Line')
    child_ids = fields.Many2many(
        'res.users', 'res_user_first_rel1',
        'user_id', 'res_user_second_rel1', string='Childs')
    dept_id = fields.Many2one('op.department', string='Department Name')
    department_ids = fields.Many2many('op.department',
                                      string='Allowed Department')
    department_count = fields.Integer(compute='_compute_department_count',
                                      string="Number of Departments",
                                      default=_department_count)

    def create_user(self, records, user_group=None):
        for rec in records:
            if not rec.user_id:
                user_vals = {
                    'name': rec.name,
                    'login': rec.email or (rec.name + rec.last_name),
                    'partner_id': rec.partner_id.id,
                    'dept_id': rec.main_department_id.id,
                    'department_ids': rec.allowed_department_ids.ids
                }
                user_id = self.create(user_vals)
                rec.user_id = user_id
                if user_group:
                    user_group.users = user_group.users + user_id

    def _compute_department_count(self):
        department_count = self._department_count()
        for user in self:
            user.department_count = department_count
