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
import time

class op_book_queue(osv.osv):
    _name = 'op.book.queue'
    _rec_name = 'partner_id'
    
    _description = """ Book Queue Request Detail for Students and Faculties """
    
    _columns = {
            'name':fields.char("Sequence No",readonly=True,copy=False),
            'partner_id': fields.many2one('res.partner', 'Student/Faculty', required=True),
            'book_id': fields.many2one('op.book', 'Book', required=True),
            'date_from': fields.date('From Date', required=True),
            'date_to': fields.date('To Date', required=True),
            'user_id' : fields.many2one('res.users',readonly=True,string="User"),
            'state': fields.selection([('request','Request'),('accept','Accept'),\
                                       ('reject','Reject')], 'Status',copy=False),
    }
    _defaults = {
                 'state': 'request',
                 'name': '/',
                 'user_id': lambda obj, cr, uid, context: uid,
                 }
    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if vals.get('name', '/') == '/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'op.book.queue') or '/'
        return super(op_book_queue, self).create(cr, uid, vals, context=context)
    
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
