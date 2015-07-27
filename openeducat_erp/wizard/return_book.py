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


class ReturnBook(models.TransientModel):

    """ Retrun Book Wizard """
    _name = 'return.book'

    book_id = fields.Many2one('op.book', 'Book', readonly=True)
    actual_return_date = fields.Date(
        'Actual Return Date', default=lambda self: fields.Date.today(),
        required=True)

    @api.one
    def do_return(self):
        book_movement = self.env['op.book.movement']
        if self.book_id.state and self.book_id.state == 'i':
            book_move_search = book_movement.search(
                [('book_id', '=', self.book_id.id), ('state', '=', 'i')])
            if not book_move_search:
                return {'type': 'ir.actions.act_window_close'}
            book_move_search.actual_return_date = self.actual_return_date
            book_move_search.calculate_penalty()
            self.book_id.state = 'a'
        else:
            book_state = self.book_id.state == 'i' and 'Issued' or \
                self.book_id.state == 'a' and 'Available' or \
                self.book_id.state == 'l' and 'Lost' or \
                self.book_id.state == 'r' and 'Reserved'
            raise Warning(_('Error!'), _(
                'Book Can not be issued because book state is : %s') %
                (book_state))


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
