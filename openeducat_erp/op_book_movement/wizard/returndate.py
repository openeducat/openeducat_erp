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
from openerp.osv import osv, fields
from openerp.tools.translate import _
import time

class return_date(osv.osv_memory):
    """ Assign return date """

    _name = 'return.date'

    _columns = {
        'actual_return_date': fields.date(string='Actual Return Date', required=True),
    }

    _defaults = {'actual_return_date': time.strftime("%Y-%m-%d")}

    def assign_return_date(self, cr, uid, ids, context={}):
        value = {}
        book_movement = self.pool.get("op.book.movement")
        book_movement.write(cr, uid, context.get('active_ids',False),
                            {'actual_return_date': self.browse(cr, uid, ids[0]).actual_return_date})
        book_movement.calculate_penalty(cr, uid, context.get('active_ids',False), context)
        value = {'type': 'ir.actions.act_window_close'}
        return value


return_date()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
