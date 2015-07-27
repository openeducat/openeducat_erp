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

from openerp import models, fields, api, _
from openerp.exceptions import Warning


class OpFaculty(models.Model):
    _name = 'op.faculty'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one(
        'res.partner', 'Partner', required=True, ondelete="cascade")
    middle_name = fields.Char('Middle Name', size=128, required=True)
    last_name = fields.Char('Last Name', size=128, required=True)
    birth_date = fields.Date('Birth Date', required=True)
    blood_group = fields.Selection(
        [('A+', 'A+ve'), ('B+', 'B+ve'), ('O+', 'O+ve'), ('AB+', 'AB+ve'),
         ('A-', 'A-ve'), ('B-', 'B-ve'), ('O-', 'O-ve'), ('AB-', 'AB-ve')],
        'Blood Group')
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')], 'Gender', required=True)
    nationality = fields.Many2one('res.country', 'Nationality')
    language = fields.Many2one('res.lang', 'Language')
    category = fields.Many2one('op.category', 'Category', required=True)
    religion = fields.Many2one('op.religion', 'Religion')
    library_card = fields.Char('Library Card', size=64)
    emergency_contact = fields.Many2one(
        'res.partner', 'Emergency Contact')
    pan_card = fields.Char('PAN Card', size=64)
    bank_acc_num = fields.Char('Bank Acc Number', size=64)
    visa_info = fields.Char('Visa Info', size=64)
    id_number = fields.Char('ID Card Number', size=64)
    photo = fields.Binary('Photo')
    login = fields.Char(
        'Login', related='partner_id.user_id.login', readonly=1)
    last_login = fields.Date(
        'Latest Connection', related='partner_id.user_id.login_date',
        readonly=1)
    timetable_ids = fields.One2many('op.timetable', 'faculty_id', 'Time table')
    health_faculty_lines = fields.One2many(
        'op.health', 'faculty_id', 'Health Detail')
    faculty_subject_ids = fields.Many2many('op.subject', string='Subjects')
    emp_id = fields.Many2one('hr.employee', 'Employee')

    @api.one
    def create_employee(self):
        emp_obj = self.env['hr.employee']
        vals = {
            'name': self.name + ' ' + self.middle_name + ' ' + self.last_name,
            'country_id': self.nationality.id,
            'gender': self.gender,
        }
        emp_id = emp_obj.create(vals)
        self.write({'emp_id': emp_id.id})


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.onchange('user_id')
    def onchange_user(self):
        if self.user_id:
            self.user_id.partner_id.supplier = True
            self.address_home_id = self.user_id.partner_id.id
            self.work_email = self.user_id.email
            self.identification_id = False
            return {'domain':
                    {'address_id': [('id', '=', self.user_id.partner_id.id)]}}

    @api.onchange('address_id')
    def onchange_address_id(self):
        if self.address_home_id and self.address_id and \
                self.address_home_id != self.address_id:
            raise Warning(_('Configuration Error!'), _(
                'Home Address and working address should be same!'))
        if self.address_id:
            self.work_phone = self.address_id.phone
            self.mobile_phone = self.address_id.mobile

    @api.onchange('address_home_id')
    def onchange_address_home_id(self):
        if self.address_home_id and self.address_id and \
                self.address_home_id != self.address_id:
            raise Warning(_('Configuration Error!'), _(
                'Home Address and working address should be same!'))
        if self.address_home_id:
            self.address_home_id.write({'supplier': True, 'employee': True})


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
