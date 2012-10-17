# -*- coding: utf-8 -*-
#/#############################################################################
#    
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2004-TODAY Tech-Receptives(<http://www.tech-receptives.com>).
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
#/#############################################################################
from osv import osv, fields
from tools.translate import _
import time

class return_book(osv.osv_memory):
    """ Retrun Book Wizard """

    _name = 'return.book'

    _columns = {
                'book_id': fields.many2one('op.book', string='Book', readonly=True),
                'actual_return_date': fields.date(string='Actual Return Date', required=True),
                }
    
    _defaults = {'actual_return_date': time.strftime('%Y-%m-%d')}
    
    def do_return(self, cr, uid, ids, context={}):
        value = {}
        book_movement = self.pool.get("op.book.movement")
        for this_obj in self.browse(cr, uid, ids):
            if this_obj.book_id.status and this_obj.book_id.status == 'I':
                book_move_search = book_movement.search(cr, uid, [('book_id','=',this_obj.book_id.id),('state','=','I')])
                if not book_move_search: value = {'type': 'ir.actions.act_window_close'}
                book_movement.write(cr, uid, book_move_search,
                                {'actual_return_date': this_obj.actual_return_date})
                book_movement.calculate_penalty(cr, uid, book_move_search, context)
            else:
                book_state = this_obj.book_id.status == 'I' and 'Issued' or \
                              this_obj.book_id.status == 'a' and 'Available' or \
                              this_obj.book_id.status == 'L' and 'Lost' or \
                              this_obj.book_id.status == 'r' and 'Reserved'
                raise osv.except_osv(('Error!'),("Book Can not be issued because book state is : %s") %(book_state))
        return value
    
return_book()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
