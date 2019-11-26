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

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class OpStudentCourse(models.Model):
    _name = "op.student.course"
    _description = "Student Course Details"

    student_id = fields.Many2one('op.student', 'Student', ondelete="cascade")
    course_id = fields.Many2one('op.course', 'Course', required=True)
    batch_id = fields.Many2one('op.batch', 'Batch', required=True)
    roll_number = fields.Char('Roll Number')
    subject_ids = fields.Many2many('op.subject', string='Subjects')

    _sql_constraints = [
        ('unique_name_roll_number_id',
         'unique(roll_number,course_id,batch_id,student_id)',
         'Roll Number & Student must be unique per Batch!'),
        ('unique_name_roll_number_course_id',
         'unique(roll_number,course_id,batch_id)',
         'Roll Number must be unique per Batch!'),
        ('unique_name_roll_number_student_id',
         'unique(student_id,course_id,batch_id)',
         'Student must be unique per Batch!'),
    ]


class OpStudent(models.Model):
    _name = "op.student"
    _description = "Student"
    _inherit = "mail.thread"
    _inherits = {"res.partner": "partner_id"}

    middle_name = fields.Char('Middle Name', size=128)
    last_name = fields.Char('Last Name', size=128)
    birth_date = fields.Date('Birth Date')
    blood_group = fields.Selection([
        ('A+', 'A+ve'),
        ('B+', 'B+ve'),
        ('O+', 'O+ve'),
        ('AB+', 'AB+ve'),
        ('A-', 'A-ve'),
        ('B-', 'B-ve'),
        ('O-', 'O-ve'),
        ('AB-', 'AB-ve')
    ], string='Blood Group')
    gender = fields.Selection([
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Other')
    ], 'Gender', required=True, default='m')
    nationality = fields.Many2one('res.country', 'Nationality')
    emergency_contact = fields.Many2one('res.partner', 'Emergency Contact')
    visa_info = fields.Char('Visa Info', size=64)
    id_number = fields.Char('ID Card Number', size=64)
    partner_id = fields.Many2one('res.partner', 'Partner',
                                 required=True, ondelete="cascade")
    gr_no = fields.Char("GR Number", size=20)
    category_id = fields.Many2one('op.category', 'Category')
    course_detail_ids = fields.One2many('op.student.course', 'student_id',
                                        'Course Details',
                                        track_visibility='onchange')

    _sql_constraints = [(
        'unique_gr_no',
        'unique(gr_no)',
        'GR Number must be unique per student!'
    ), ('unique_partner',
        'unique(partner_id)',
        'Partner was already linked!')]

    @api.multi
    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            if record.birth_date > fields.Date.today():
                raise ValidationError(_(
                    "Birth Date can't be greater than current date!"))

    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Students'),
            'template': '/openeducat_core/static/xls/op_student.xls'
        }]

    @api.multi
    def create_student_user(self):
        user_group = self.env.ref("base.group_portal") or False
        users_res = self.env['res.users']
        for record in self:
            if not record.user_id:
                user_id = users_res.create({
                    'name': record.name,
                    'partner_id': record.partner_id.id,
                    'login': record.email,
                    'groups_id': user_group,
                    'is_student': True,
                    'tz': self._context.get('tz')
                })
                record.user_id = user_id

    complete_name = fields.Char('Complete Name', compute='_compute_complete_name', store=True)

    @api.depends('name', 'middle_name', 'last_name')
    def _compute_complete_name(self):
        for stud in self:
            complete_name = stud.name
            if stud.middle_name:
                complete_name = '%s %s' % (complete_name, stud.middle_name)
            if stud.last_name:
                complete_name = '%s %s' % (complete_name, stud.last_name)
            stud.complete_name = complete_name

    @api.model
    def create(self, vals):
        vals['is_student'] = True
        vals['customer'] = True
        if vals.get('name'):
            vals['name'] = ' '.join(vals['name'].split())
        if vals.get('middle_name'):
            vals['middle_name'] = ' '.join(vals['middle_name'].split())
        if vals.get('last_name'):
            vals['last_name'] = ' '.join(vals['last_name'].split())

        student = super(OpStudent, self).create(vals)

        if vals.get('middle_name') or vals.get('last_name'):
            student.partner_id._compute_display_name()

        return student

    @api.multi
    def write(self, vals):
        if vals.get('name'):
            vals['name'] = ' '.join(vals['name'].split())
        if vals.get('middle_name'):
            vals['middle_name'] = ' '.join(vals['middle_name'].split())
        if vals.get('last_name'):
            vals['last_name'] = ' '.join(vals['last_name'].split())

        student = super(OpStudent, self).write(vals)

        if vals.get('middle_name') or vals.get('last_name'):
            self.partner_id._compute_display_name()

        return student
