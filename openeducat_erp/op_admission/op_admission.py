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


class OpAdmission(models.Model):
    _name = 'op.admission'
    _rec_name = 'application_number'
    _order = "application_number desc"

    name = fields.Char(
        'First Name', size=128, required=True,
        states={'done': [('readonly', True)]})
    middle_name = fields.Char(
        'Middle Name', size=128, required=True,
        states={'done': [('readonly', True)]})
    last_name = fields.Char(
        'Last Name', size=128, required=True,
        states={'done': [('readonly', True)]})
    title = fields.Many2one(
        'res.partner.title', 'Title', states={'done': [('readonly', True)]})
    application_number = fields.Char(
        'Application Number', size=16, required=True, copy=False,
        states={'done': [('readonly', True)]},
        default=lambda self: self.env['ir.sequence'].get('op.admission'))
    admission_date = fields.Date(
        'Admission Date', required=True, copy=False,
        states={'done': [('readonly', True)]},
        default=lambda self: fields.Date.today())
    application_date = fields.Datetime(
        'Application Date', required=True, copy=False,
        states={'done': [('readonly', True)]},
        default=lambda self: fields.Datetime.now())
    birth_date = fields.Date(
        'Birth Date', required=True, states={'done': [('readonly', True)]})
    course_id = fields.Many2one(
        'op.course', 'Course', required=True,
        states={'done': [('readonly', True)]})
    batch_id = fields.Many2one(
        'op.batch', 'Batch', required=True,
        states={'done': [('readonly', True)]})
    street = fields.Char(
        'Street', size=256, states={'done': [('readonly', True)]})
    street2 = fields.Char(
        'Street2', size=256, states={'done': [('readonly', True)]})
    phone = fields.Char(
        'Phone', size=16, states={'done': [('readonly', True)]})
    mobile = fields.Char(
        'Mobile', size=16, states={'done': [('readonly', True)]})
    email = fields.Char(
        'Email', size=256, states={'done': [('readonly', True)]})
    city = fields.Char('City', size=64, states={'done': [('readonly', True)]})
    zip = fields.Char('Zip', size=8, states={'done': [('readonly', True)]})
    state_id = fields.Many2one(
        'res.country.state', 'States', states={'done': [('readonly', True)]})
    country_id = fields.Many2one(
        'res.country', 'Country', states={'done': [('readonly', True)]})
    fees = fields.Float('Fees', states={'done': [('readonly', True)]})
    photo = fields.Binary('Photo', states={'done': [('readonly', True)]})
    state = fields.Selection(
        [('d', 'Draft'), ('i', 'Confirm'), ('s', 'Enroll'), ('done', 'Done'),
         ('r', 'Rejected'), ('p', 'Pending'), ('c', 'Cancel')], 'State',
        readonly=True, select=True, default='d')
    due_date = fields.Date('Due Date', states={'done': [('readonly', True)]})
    prev_institute = fields.Char(
        'Previous Institute', size=256, states={'done': [('readonly', True)]})
    prev_course = fields.Char(
        'Previous Course', size=256, states={'done': [('readonly', True)]})
    prev_result = fields.Char(
        'Previous Result', size=256, states={'done': [('readonly', True)]})
    family_business = fields.Char(
        'Family Business', size=256, states={'done': [('readonly', True)]})
    family_income = fields.Float(
        'Family Income', states={'done': [('readonly', True)]})
    religion_id = fields.Many2one(
        'op.religion', 'Religion', states={'done': [('readonly', True)]})
    category_id = fields.Many2one(
        'op.category', 'Category', required=True,
        states={'done': [('readonly', True)]})
    gender = fields.Selection(
        [('m', 'Male'), ('f', 'Female'), ('o', 'Other')], 'Gender',
        required=True, states={'done': [('readonly', True)]})
    standard_id = fields.Many2one(
        'op.standard', 'Standard', required=True,
        states={'done': [('readonly', True)]})
    division_id = fields.Many2one(
        'op.division', 'Division', states={'done': [('readonly', True)]})
    student_id = fields.Many2one(
        'op.student', 'Student', states={'done': [('readonly', True)]})
    nbr = fields.Integer('# of Admission', readonly=True)
    gr_no = fields.Boolean('Old Student??')
    gr_no_old = fields.Char('GR Number old', size=10)
    gr_no_new = fields.Char('GR Number new', size=10)

    @api.one
    def confirm_in_progress(self):
        self.state = 'i'

    @api.one
    def confirm_selection(self):
        gr = self.gr_no_new
        if self.gr_no:
            gr = self.gr_no_old
        vals = {
            'title': self.title and self.title.id or False,
            'name': self.name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date,
            'gender': self.gender,
            'category': self.category_id and self.category_id.id or False,
            'course_id': self.course_id and self.course_id.id or False,
            'batch_id': self.batch_id and self.batch_id.id or False,
            'standard_id': self.standard_id and self.standard_id.id or False,
            'religion': self.religion_id and self.religion_id.id or False,
            'photo': self.photo or False,
            'gr_no': gr,
            'street': self.street or False,
            'street2': self.street2 or False,
            'phone': self.phone or False,
            'mobile': self.mobile or False,
            'zip': self.zip or False,
            'city': self.city or False,
            'country_id': self.country_id and self.country_id.id or False,
            'state_id': self.state_id and self.state_id.id or False,
        }
        self.write({
            'state': 's',
            'student_id': self.env['op.student'].create(vals).id,
            'nbr': 1
        })

    @api.one
    def fee_paid(self):
        # TO_FIX:: Remove this method & its call from YML as it's not used.
        self.state = 'd'

    @api.one
    def confirm_rejected(self):
        self.state = 'r'

    @api.one
    def confirm_pending(self):
        self.state = 'p'

    @api.one
    def confirm_to_draft(self):
        self.state = 'd'
        self.delete_workflow()
        self.create_workflow()

    @api.one
    def confirm_cancel(self):
        self.state = 'c'

    @api.multi
    def open_student(self):
        form_view = self.env.ref('openeducat_erp.view_op_student_form')
        tree_view = self.env.ref('openeducat_erp.view_op_student_tree')
        value = {
            'domain': str([('id', '=', self.student_id.id)]),
            'view_type': 'form',
            'view_mode': 'tree, form',
            'res_model': 'op.student',
            'view_id': False,
            'views': [(form_view and form_view.id or False, 'form'),
                      (tree_view and tree_view.id or False, 'tree')],
            'type': 'ir.actions.act_window',
            'res_id': self.student_id.id,
            'target': 'current',
            'nodestroy': True
        }
        self.state = 'done'
        return value

    @api.one
    def create_student_invoice(self):
        self.student_id.create_invoice()
        self.state = 'done'

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
