# -*- coding: utf-8 -*-
##############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech Receptives(<http://www.techreceptives.com>).
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
##############################################################################

from openerp import models, fields, api
from openerp.exceptions import ValidationError


class OpAdmission(models.Model):
    _name = 'op.admission'
    _inherit = 'mail.thread'
    _rec_name = 'application_number'
    _order = "application_number desc"
    _description = "Admission"

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
        default=lambda self:
        self.env['ir.sequence'].next_by_code('op.admission'))
    admission_date = fields.Date(
        'Admission Date', copy=False,
        states={'done': [('readonly', True)]})
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
        'op.batch', 'Batch', required=False,
        states={'done': [('readonly', True)],
                'fees_paid': [('required', True)]})
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
        [('draft', 'Draft'), ('confirm', 'Confirmed'),
         ('payment_process', 'Payment Process'), ('fees_paid', 'Fees Paid'),
         ('reject', 'Rejected'), ('pending', 'Pending'),
         ('cancel', 'Cancelled'), ('done', 'Done')],
        'State', readonly=True, select=True,
        default='draft', track_visibility='onchange')
    due_date = fields.Date('Due Date', states={'done': [('readonly', True)]})
    prev_institute_id = fields.Many2one(
        'res.partner', 'Previous Institute',
        states={'done': [('readonly', True)]})
    prev_course_id = fields.Many2one(
        'op.course', 'Previous Course', states={'done': [('readonly', True)]})
    prev_result = fields.Char(
        'Previous Result', size=256, states={'done': [('readonly', True)]})
    family_business = fields.Char(
        'Family Business', size=256, states={'done': [('readonly', True)]})
    family_income = fields.Float(
        'Family Income', states={'done': [('readonly', True)]})
    gender = fields.Selection(
        [('m', 'Male'), ('f', 'Female'), ('o', 'Other')], 'Gender',
        required=True, states={'done': [('readonly', True)]})
    student_id = fields.Many2one(
        'op.student', 'Student', states={'done': [('readonly', True)]})
    nbr = fields.Integer('No of Admission', readonly=True)
    register_id = fields.Many2one(
        'op.admission.register', 'Admission Register', required=True,
        states={'done': [('readonly', True)]})
    partner_id = fields.Many2one('res.partner', 'Partner')

    @api.onchange('register_id')
    def onchange_register(self):
        self.course_id = self.register_id.course_id
        self.fees = self.register_id.product_id.lst_price

    @api.one
    @api.constrains('register_id', 'application_date')
    def _check_admission_register(self):
        start_date = fields.Date.from_string(self.register_id.start_date)
        end_date = fields.Date.from_string(self.register_id.end_date)
        application_date = fields.Date.from_string(self.application_date)
        if application_date < start_date or application_date > end_date:
            raise ValidationError(
                "Application Date should be between Start Date & \
                End Date of Admission Register.")

    @api.one
    def confirm_in_progress(self):
        self.state = 'confirm'
        if self.partner_id:
            self.state = 'payment_process'

    @api.multi
    def get_student_vals(self):
        return {
            'title': self.title and self.title.id or False,
            'name': self.name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date,
            'gender': self.gender,
            'course_id': self.course_id and self.course_id.id or False,
            'batch_id': self.batch_id and self.batch_id.id or False,
            'photo': self.photo or False,
            'street': self.street or False,
            'street2': self.street2 or False,
            'phone': self.phone or False,
            'mobile': self.mobile or False,
            'zip': self.zip or False,
            'city': self.city or False,
            'country_id': self.country_id and self.country_id.id or False,
            'state_id': self.state_id and self.state_id.id or False,
        }

    @api.one
    def enroll_student(self):
        total_admission = self.env['op.admission'].search_count(
            [('register_id', '=', self.register_id.id),
             ('state', '=', 'done')])
        if self.register_id.max_count:
            if not total_admission < self.register_id.max_count:
                msg = 'Max Admission In Admission Register :- (%s)' % (
                    self.register_id.max_count)
                raise ValidationError(msg)

        vals = self.get_student_vals()
        vals.update({'partner_id': self.partner_id.id})
        self.write({
            'nbr': 1,
            'state': 'done',
            'admission_date': fields.Date.today(),
            'student_id': self.env['op.student'].create(vals).id,
        })

    @api.one
    def confirm_rejected(self):
        self.state = 'reject'

    @api.one
    def confirm_pending(self):
        self.state = 'pending'

    @api.one
    def confirm_to_draft(self):
        self.state = 'draft'

    @api.one
    def confirm_cancel(self):
        self.state = 'cancel'

    @api.one
    def payment_process(self):
        self.state = 'fees_paid'

    @api.multi
    def open_student(self):
        form_view = self.env.ref('openeducat_core.view_op_student_form')
        tree_view = self.env.ref('openeducat_core.view_op_student_tree')
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

    @api.multi
    def create_invoice(self):
        """ Create invoice for fee payment process of student """

        invoice_pool = self.env['account.invoice']
        invoice_line_pool = self.env['account.invoice.line']

        partner_id = self.env['res.partner'].create({'name': self.name})

        invoice_fields = invoice_pool.fields_get(self)
        invoice_default = invoice_pool.default_get(invoice_fields)

        line_fields = invoice_line_pool.fields_get(self)
        invoice_line_default = invoice_line_pool.default_get(line_fields)

        type = 'out_invoice'
        onchange_partner = invoice_pool.onchange_partner_id(
            type, partner_id.id)
        invoice_default.update(onchange_partner['value'])

        invoice_data = {
            'partner_id': partner_id.id,
            'date_invoice': fields.Date.today(),
            'payment_term': self.course_id.payment_term and
            self.course_id.payment_term.id or False,
        }
        invoice_default.update(invoice_data)
        invoice_id = invoice_pool.create(invoice_default).id

        onchange_producat = invoice_line_pool.product_id_change(
            self.register_id.product_id.id, False, 0, '', type, partner_id.id)
        invoice_line_default.update(onchange_producat['value'])
        line_data = {'product_id': self.register_id.product_id.id,
                     'price_unit': self.fees,
                     'invoice_id': invoice_id}
        invoice_line_default.update(line_data)
        invoice_line_pool.create(invoice_line_default).id

        self.write({'invoice_ids': [(4, invoice_id)]})
        form_view = self.env.ref('account.invoice_form')
        tree_view = self.env.ref('account.invoice_tree')
        value = {
            'domain': str([('id', '=', invoice_id)]),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.invoice',
            'view_id': False,
            'views': [(form_view and form_view.id or False, 'form'),
                      (tree_view and tree_view.id or False, 'tree')],
            'type': 'ir.actions.act_window',
            'res_id': invoice_id,
            'target': 'current',
            'nodestroy': True
        }
        self.partner_id = partner_id
        self.state = 'payment_process'
        return value


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
