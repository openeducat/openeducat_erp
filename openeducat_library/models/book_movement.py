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

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


def days_between(to_date, from_date):
    to_date = fields.Datetime.from_string(to_date)
    from_date = fields.Datetime.from_string(from_date)
    return abs((from_date - to_date).days)


class OpBookMovement(models.Model):
    _name = 'op.book.movement'
    _inherit = 'mail.thread'
    _description = 'Book Movement'
    _rec_name = 'book_id'

    book_id = fields.Many2one('op.book', 'Book', required=True)
    book_unit_id = fields.Many2one(
        'op.book.unit', 'Book Unit', required=True,
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
    return_date = fields.Date('Return Date', required=True)
    actual_return_date = fields.Date('Actual Return Date')
    penalty = fields.Float('Penalty')
    partner_id = fields.Many2one(
        'res.partner', 'Person', track_visibility='onchange')
    reserver_name = fields.Char('Person Name', size=256)
    state = fields.Selection(
        [('available', 'Available'), ('reserve', 'Reserved'),
         ('issue', 'Issued'), ('lost', 'Lost'),
         ('return', 'Returned')], 'Status',
        default='available', track_visibility='onchange')

    @api.constrains('issued_date', 'return_date')
    def _check_date(self):
        if self.issued_date > self.return_date:
            raise ValidationError(
                'Return Date cannot be set before Issued Date.')

    @api.constrains('issued_date', 'actual_return_date')
    def check_actual_return_date(self):
        if self.actual_return_date:
            if self.issued_date > self.actual_return_date:
                raise ValidationError(
                    'Actual Return Date cannot be set before Issued Date')

    @api.onchange('book_unit_id')
    def onchange_book_unit_id(self):
        self.state = self.book_unit_id.state

    @api.onchange('library_card_id')
    def onchange_library_card_id(self):
        self.type = self.library_card_id.type
        self.student_id = self.library_card_id.student_id.id
        self.faculty_id = self.library_card_id.faculty_id.id

    @api.one
    def issue_book(self):
        ''' function to issue book '''
        if self.book_unit_id.state and self.book_unit_id.state == 'available':
            self.book_unit_id.state = 'issue'
            self.state = 'issue'

    @api.one
    def calculate_penalty(self):
        penalty_amt = 0
        penalty_days = 0
        standard_diff = days_between(self.return_date, self.issued_date)
        actual_diff = days_between(self.actual_return_date, self.issued_date)
        owned_days = standard_diff + \
            self.library_card_id.library_card_type_id.duration
        if self.library_card_id and self.library_card_id.library_card_type_id:
            penalty_days = actual_diff > owned_days and actual_diff - \
                owned_days or penalty_days
            penalty_amt = round(penalty_days - penalty_days / 7) * \
                self.library_card_id.library_card_type_id.penalty_amt_per_day
        self.write({'penalty': penalty_amt})

    @api.multi
    def return_book(self):
        ''' function to return book '''
        if self.book_unit_id.state and self.book_unit_id.state == 'issue':
            return {
                'name': _('Return Date'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'return.date',
                'type': 'ir.actions.act_window',
                'target': 'new',
            }
        return True

    @api.multi
    def do_book_reservation(self):
        ''' function to reserve book '''
        return {
            'name': _('Book Reservation'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'reserve.book',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
