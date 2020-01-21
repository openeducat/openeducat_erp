# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
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

from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = "res.company"

    signature = fields.Binary('Signature')
    accreditation = fields.Text('Accreditation')
    approval_authority = fields.Text('Approval Authority')


class ResUsers(models.Model):
    _inherit = "res.users"

    user_line = fields.One2many('op.student', 'user_id', 'User Line')
    child_ids = fields.Many2many(
        'res.users', 'res_user_first_rel1',
        'user_id', 'res_user_second_rel1', string='Childs')

    @api.multi
    def create_user(self, records, user_group=None):
        for rec in records:
            if not rec.user_id:
                user_vals = {
                    'name': rec.name,
                    'login': rec.email or (rec.name + rec.last_name),
                    'partner_id': rec.partner_id.id
                }
                user_id = self.create(user_vals)
                rec.user_id = user_id
                if user_group:
                    user_group.users = user_group.users + user_id

    def search_read_for_app(self, domain=None, fields=None, offset=0, limit=None, order=None):
        if self.env.user.partner_id.is_student:
            domain = ([('user_id', '=', self.env.user.id)])
            user = self.sudo().search_read(domain=domain, fields=['name', 'email', 'image',
                                                                  'mobile', 'country_id', 'city', 'street', 'state_id',
                                                                  'zip'], offset=offset, limit=limit, order=order)
            student = self.env['op.student'].sudo().search([('user_id', '=', self.env.user.id)])
            res = {'user_data': user,
                   'birth_date': student.birth_date,
                   'blood_group': student.blood_group,
                   'gender': student.gender,
                   'student_id': student.id
                   }
            return res

        elif self.env.user.partner_id.is_parent:
            domain = ([('user_id', '=', self.env.user.id)])
            res = self.sudo().search_read(domain=domain, fields=['name', 'email', 'image', 'mobile', 'country_id',
                                                                 'city', 'street', 'state_id', 'zip'], offset=offset,
                                          limit=limit, order=order)
            return {'user_data': res}

        else:
            domain = ([('user_id', '=', self.env.user.id)])
            user = self.sudo().search_read(domain=domain, fields=['name', 'email', 'image', 'mobile', 'country_id',
                                                                  'city', 'street', 'state_id', 'zip'],
                                           offset=offset, limit=limit, order=order)
            faculty = self.env['op.faculty'].sudo().search([('user_id', '=', self.env.user.id)])
            res = {'user_data': user,
                   'faculty_id': faculty.id,
                   'birth_date': faculty.birth_date,
                   'blood_group': faculty.blood_group,
                   'gender': faculty.gender}
            return res
