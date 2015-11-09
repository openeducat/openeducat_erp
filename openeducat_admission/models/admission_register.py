# -*- coding: utf-8 -*-
##############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech Receptives(<http://www.techreceptives.com>).
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
##############################################################################

from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp import models, fields, api
from openerp.exceptions import ValidationError


class OpAdmissionRegister(models.Model):
    _name = 'op.admission.register'
    _inherit = 'mail.thread'
    _description = 'Admission Register'

    name = fields.Char(
        'Name', required=True, readonly=True,
        states={'draft': [('readonly', False)]})
    start_date = fields.Date(
        'Start Date', required=True, readonly=True,
        default=fields.Date.today(), states={'draft': [('readonly', False)]})
    end_date = fields.Date(
        'End Date', required=True, readonly=True,
        default=(datetime.today() + relativedelta(days=30)),
        states={'draft': [('readonly', False)]})
    course_id = fields.Many2one(
        'op.course', 'Course', required=True, readonly=True,
        states={'draft': [('readonly', False)]}, track_visibility='onchange')
    min_count = fields.Integer(
        'Minimum No. of Admission', readonly=True,
        states={'draft': [('readonly', False)]})
    max_count = fields.Integer(
        'Maximum No. of Admission', readonly=True,
        states={'draft': [('readonly', False)]}, default=30)
    product_id = fields.Many2one(
        'product.product', 'Product', required=True,
        domain=[('type', '=', 'service')], readonly=True,
        states={'draft': [('readonly', False)]}, track_visibility='onchange')
    admission_ids = fields.One2many(
        'op.admission', 'register_id', 'Admissions')
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirmed'),
         ('cancel', 'Cancelled'), ('application', 'Application Gathering'),
         ('admission', 'Admission Process'), ('done', 'Done')],
        'Status',  default='draft', track_visibility='onchange')

    @api.one
    @api.constrains('start_date', 'end_date')
    def check_dates(self):
        start_date = fields.Date.from_string(self.start_date)
        end_date = fields.Date.from_string(self.end_date)
        if start_date > end_date:
            raise ValidationError("End Date cannot be set before Start Date.")

    @api.one
    @api.constrains('min_count', 'max_count')
    def check_no_of_admission(self):
        if (self.min_count < 0) or (self.max_count < 0):
            raise ValidationError("No of Admission should be positive!")
        if self.min_count > self.max_count:
            raise ValidationError(
                "Min Admission can't be greater than Max Admission")

    @api.one
    def confirm_register(self):
        self.state = 'confirm'

    @api.one
    def set_to_draft(self):
        self.state = 'draft'

    @api.one
    def cancel_register(self):
        self.state = 'cancel'

    @api.one
    def start_application(self):
        self.state = 'application'

    @api.one
    def start_admission(self):
        self.state = 'admission'

    @api.one
    def close_register(self):
        self.state = 'done'


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
