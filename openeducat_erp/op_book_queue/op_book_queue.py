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
import time

class op_book_queue(osv.osv):
    _name = 'op.book.queue'
    
    _description = """ Book Queue Request Detail for Students and Faculties """
    
    _columns = {
            'partner_id': fields.many2one('res.partner', 'Student/Faculty', required=True),
#            'book_id': fields.many2one('op.book', 'Book', required=True),
            'book_ids': fields.many2many('op.book', 'op_queue_book_rl', 'op_book_id', 'op_queue_id', 'Book'),
            'date_from': fields.date('From Date', required=True),
            'date_to': fields.date('To Date', required=True),
            'state': fields.selection([('request','Request'),('accept','Accept'),\
                                       ('reject','Reject')], 'Status'),
    }

    _defaults = {'state': 'request'}

    def do_reject(self, cr, uid, ids, context={}):
        self.write(cr, uid, ids, {'state': 'reject'})
        return True

    def do_accept(self, cr, uid, ids, context={}):
        self.write(cr, uid, ids, {'state': 'accept'})
        return True
    
    def do_request_again(self, cr, uid, ids, context={}):
        self.write(cr, uid, ids, {'state': 'request'})
        return True

op_book_queue()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
