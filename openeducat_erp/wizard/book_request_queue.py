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

from openerp.osv import osv, fields


class BookRequestQueue(osv.TransientModel):

    _name = 'book.request.queue'

    _columns = {
        'date_from': fields.date('From Date', required=True),
        'date_to': fields.date('To Date', required=True),
        'book_id': fields.many2one('op.book', 'Book'),
    }

    def add_book_request_queue(self, cr, uid, ids, context=None):
        value = {}

        queue_pool = self.pool.get('op.book.queue')
        book_pool = self.pool.get('op.book')

        for this_obj in self.browse(cr, uid, ids, context):
            queue_data = {
                'partner_id': self.pool.get('res.users').browse(
                    cr, uid, uid, context).partner_id.id,
                'date_from': this_obj.date_from,
                'date_to': this_obj.date_to,
            }

            id_book = book_pool.read(
                cr, uid, this_obj.book_id.id, ['id_book'])['id_book']

            if id_book:
                search_book = book_pool.search(
                    cr, uid, [('id_book', '=', id_book)])

                if search_book:
                    queue_data.update({'book_ids': [(6, 0, search_book)]})

            else:
                queue_data.update(
                    {'book_ids': [(6, 0, [this_obj.book_id.id])]})

            queue_pool.create(cr, uid, queue_data, context)

            value = {'type': 'ir.actions.act_window_close'}
        return value


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
