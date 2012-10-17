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
from datetime import datetime
from tools.translate import _

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

class op_book_movement(osv.osv):
    _name = 'op.book.movement'
    _rec_name = 'book_id'
    
    _columns = {
            'book_id': fields.many2one('op.book', string='Book', required=True),
            'student_id': fields.many2one('op.student', string='Student', required=True),
            'library_card_id': fields.many2one('op.library.card', 'Library Card', required=True),
            'issued_date': fields.date(string='Issued Date', required=True),
            'return_date': fields.date(string='Return Date', required=True),
            'actual_return_date': fields.date(string='Actual Return Date'),
            'penalty': fields.float(string='Penalty'),
            'partner_id': fields.many2one('res.partner', 'Person'),
            'reserver_name': fields.char('Person Name', size=256),
            'state': fields.selection([('I','Issued'),('a','Available'),('L','Lost'),('r','Reserved')], string='Status'),
    }

    _defaults = {'state': 'a'}

    def issue_book(self, cr, uid, ids, context={}):
        ''' function to issuing book '''
        book_pool = self.pool.get('op.book')
        for obj in self.browse(cr, uid, ids, context):
            if obj.book_id.status and obj.book_id.status == 'a':
                book_pool.write(cr, uid, obj.book_id.id, {'status': 'I'})
                self.write(cr, uid, obj.id, {'state': 'I'})
            else:
                book_state = obj.book_id.status == 'I' and 'Issued' or \
                              obj.book_id.status == 'a' and 'Available' or \
                              obj.book_id.status == 'L' and 'Lost' or \
                              obj.book_id.status == 'r' and 'Reserved'
                raise osv.except_osv(('Error!'),("Book Can not be issued because book state is : %s") %(book_state))
        return True
    
    def calculate_penalty(self, cr, uid, obj, context={}):
        book_pool = self.pool.get('op.book')
        penalty_amt = 0
        penalty_days = 0
        for obj in self.browse(cr, uid, obj, context):
            standard_diff = days_between(obj.return_date,obj.issued_date)
            actual_diff = days_between(obj.actual_return_date,obj.issued_date)
            
            penalty_days = actual_diff > (standard_diff + obj.library_card_id.library_card_type_id.duration) and actual_diff - (standard_diff + obj.library_card_id.library_card_type_id.duration) or penalty_days
            
            penalty_amt = round(penalty_days - penalty_days/7) * obj.library_card_id.library_card_type_id.penalty_amt_per_day
            self.write(cr, uid, obj.id, {'penalty':penalty_amt,'state': 'a'})
            book_pool.write(cr, uid, obj.book_id.id, {'status': 'a'})
        return True

    def return_book(self, cr, uid, ids, context={}):
        ''' function to returning book '''
        
        for obj in self.browse(cr, uid, ids, context):
            if obj.book_id.status and obj.book_id.status == 'I':
                #wizard call for return date
                value = {}
                data_obj = self.pool.get('ir.model.data')
                view_id = data_obj._get_id(cr, uid, 'openeducat_erp', 'return_date_act')
                value = {
                        'name': _('Return Date'),
                        'view_type': 'form',
                        'view_mode': 'form',
                        'res_model': 'return.date',
                        'type': 'ir.actions.act_window',
                        'target':'new',
                        }
                return value
            else:
                book_state = obj.book_id.status == 'I' and 'Issued' or \
                              obj.book_id.status == 'a' and 'Available' or \
                              obj.book_id.status == 'L' and 'Lost' or \
                              obj.book_id.status == 'r' and 'Reserved'
                raise osv.except_osv(('Error!'),("Book Can not be issued because book state is : %s") %(book_state))
            
        return True

    def do_book_reservation(self, cr, uid, ids, context={}):
        ''' function to reserve book '''
        value = {}
        value = {
                'name': _('Book Reservation'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'reserve.book',
                'type': 'ir.actions.act_window',
                'target':'new',
                }
        return value
op_book_movement()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
