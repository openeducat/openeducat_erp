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
from openerp.exceptions import UserError
from ..models import book_unit


class ReturnBook(models.TransientModel):

    """ Retrun Book Wizard """
    _name = 'return.book'

    book_id = fields.Many2one('op.book', 'Book', readonly=True)
    book_unit_id = fields.Many2one(
        'op.book.unit', 'Book Unit', readonly=True, required=True)
    actual_return_date = fields.Date(
        'Actual Return Date', default=lambda self: fields.Date.today(),
        required=True)

    @api.one
    def do_return(self):
        book_movement = self.env['op.book.movement']
        if self.book_unit_id.state and self.book_unit_id.state == 'issue':
            book_move_search = book_movement.search(
                [('book_unit_id', '=', self.book_unit_id.id),
                 ('state', '=', 'issue')])
            if not book_move_search:
                return {'type': 'ir.actions.act_window_close'}
            book_move_search.actual_return_date = self.actual_return_date
            book_move_search.calculate_penalty()
            book_move_search.state = 'return'
            self.book_unit_id.state = 'available'
        else:
            raise UserError(_(
                "Book Unit can not be returned because it's state is : %s") %
                (dict(book_unit.unit_states).get(self.book_unit_id.state)))


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
