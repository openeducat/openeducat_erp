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

from datetime import timedelta, date

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


def days_between(to_date, from_date):
    to_date = fields.Datetime.from_string(to_date)
    from_date = fields.Datetime.from_string(from_date)
    return abs((from_date - to_date).days)


class OpMediaMovement(models.Model):
    _name = 'op.media.movement'
    _inherit = 'mail.thread'
    _description = 'Media Movement'
    _rec_name = 'media_id'

    media_id = fields.Many2one('op.media', 'Media', required=True)
    media_unit_id = fields.Many2one(
        'op.media.unit', 'Media Unit', required=True,
        track_visibility='onchange')
    type = fields.Selection(
        [('student', 'Student'), ('faculty', 'Faculty')], 'Student/Faculty',
        required=True)
    student_id = fields.Many2one('op.student', 'Student')
    faculty_id = fields.Many2one('op.faculty', 'Faculty')
    library_card_id = fields.Many2one(
        'op.library.card', 'Library Card', required=True,
        track_visibility='onchange')
    issued_date = fields.Date(
        'Issued Date', required=True, default=fields.Date.today())
    return_date = fields.Date('Due Date', required=True)
    actual_return_date = fields.Date('Actual Return Date')
    penalty = fields.Float('Penalty')
    partner_id = fields.Many2one(
        'res.partner', 'Person', track_visibility='onchange')
    reserver_name = fields.Char('Person Name', size=256)
    state = fields.Selection(
        [('available', 'Available'), ('reserve', 'Reserved'),
         ('issue', 'Issued'), ('lost', 'Lost'),
         ('return', 'Returned'), ('return_done', 'Returned Done')], 'Status',
        default='available', track_visibility='onchange')
    media_type_id = fields.Many2one(related='media_id.media_type_id',
                                    store=True, string='Media Type')
    user_id = fields.Many2one(
        'res.users', related='student_id.user_id', string='Users')
    invoice_id = fields.Many2one('account.invoice', 'Invoice', readonly=True)

    @api.constrains('issued_date', 'return_date')
    def _check_date(self):
        if self.issued_date > self.return_date:
            raise ValidationError(_(
                'Return Date cannot be set before Issued Date.'))

    @api.constrains('issued_date', 'actual_return_date')
    def check_actual_return_date(self):
        if self.actual_return_date:
            if self.issued_date > self.actual_return_date:
                raise ValidationError(_(
                    'Actual Return Date cannot be set before Issued Date'))

    @api.onchange('media_unit_id')
    def onchange_media_unit_id(self):
        self.state = self.media_unit_id.state
        self.media_id = self.media_unit_id.media_id

    @api.onchange('library_card_id')
    def onchange_library_card_id(self):
        self.type = self.library_card_id.type
        self.student_id = self.library_card_id.student_id.id
        self.faculty_id = self.library_card_id.faculty_id.id
        self.return_date = date.today() + \
            timedelta(days=self.library_card_id.library_card_type_id.duration)

    @api.one
    def issue_media(self):
        ''' function to issue media '''
        if self.media_unit_id.state and \
                self.media_unit_id.state == 'available':
            self.media_unit_id.state = 'issue'
            self.state = 'issue'

    @api.one
    def return_media(self, return_date):
        if not return_date:
            return_date = fields.Date.today()
        self.actual_return_date = return_date
        self.calculate_penalty()
        if self.penalty > 0.0:
            self.state = 'return'
        else:
            self.state = 'return_done'
        self.media_unit_id.state = 'available'

    @api.one
    def calculate_penalty(self):
        penalty_amt = 0
        penalty_days = 0
        standard_diff = days_between(self.return_date, self.issued_date)
        actual_diff = days_between(self.actual_return_date, self.issued_date)
        if self.library_card_id and self.library_card_id.library_card_type_id:
            penalty_days = actual_diff > standard_diff and actual_diff - \
                standard_diff or penalty_days
            penalty_amt = penalty_days * \
                self.library_card_id.library_card_type_id.penalty_amt_per_day
        self.write({'penalty': penalty_amt})

    @api.multi
    def create_penalty_invoice(self):
        for rec in self:
            account_id = False
            product = self.env.ref('openeducat_library.op_product_7')
            if product.id:
                account_id = product.property_account_income_id.id
            if not account_id:
                account_id = \
                    product.categ_id.property_account_income_categ_id.id
            if not account_id:
                raise UserError(
                    _('There is no income account defined for this \
                    product: "%s". You may have to install a chart of \
                    account from Accounting app, settings \
                    menu.') % (product.name,))

            invoice = self.env['account.invoice'].create({
                'partner_id': self.student_id.partner_id.id,
                'type': 'out_invoice',
                'reference': False,
                'date_invoice': fields.Date.today(),
                'account_id':
                self.student_id.partner_id.property_account_receivable_id.id,
                'invoice_line_ids': [(0, 0, {
                    'name': product.name,
                    'account_id': account_id,
                    'price_unit': self.penalty,
                    'quantity': 1.0,
                    'discount': 0.0,
                    'uom_id': product.uom_id.id,
                    'product_id': product.id,
                })],
            })
            invoice.compute_taxes()
            invoice.action_invoice_open()
            self.invoice_id = invoice.id
