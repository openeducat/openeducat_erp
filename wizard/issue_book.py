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
#from _xmlplus.xpath.Context import Context

class issue_book(osv.osv_memory):
    """ Issue Book """

    _name = 'issue.book'

    _columns = {
                'book_id': fields.many2one('op.book', string='Book', required=True),
                'quantity': fields.integer('No. Of Books', size=256, required=True),
                'type': fields.selection([('student', 'Student'), ('faculty', 'Faculty')], 'Type', required=True),
                'student_id': fields.many2one('op.student', string='Student'),
                'faculty_id': fields.many2one('op.faculty', string='Faculty'),
                'library_card_id': fields.many2one('op.library.card', 'Library Card', required=True),
                'issued_date': fields.date(string='Issued Date', required=True),
                'return_date': fields.date(string='Return Date', required=True),
                'state': fields.selection([('i','Issued'),('a','Available'),('l','Lost'),('r','Reserved')], string='Status'),
                }

    _defaults = {
                 'state': 'i',
                 'type': 'student'
                 
                 }

    def check_issue(self, cr, uid, student_id, library_card_id, context={}):
        
        book_movement = self.pool.get("op.book.movement")
        library_card = self.pool.get("op.library.card")
        
        book_movement_search = book_movement.search(cr, uid, [('library_card_id','=',library_card_id),
                                                                  ('student_id','=',student_id),
                                                                  ('state','=','i')])
        if len(book_movement_search) < library_card.browse(cr, uid, library_card_id,context).allow_book:
            return True
        else: 
            return False
            
    def do_issue(self, cr, uid, ids, context={}):
        value = {}
        book_movement = self.pool.get("op.book.movement")
        book = self.pool.get("op.book")
        for this_obj in self.browse(cr, uid, ids,context):
            total_book = 0
            for movement in this_obj.book_id.movement_line:
                if movement.state == 'i':
                    total_book += movement.quantity
            if this_obj.book_id.number_book > 0 and this_obj.book_id.number_book - total_book > 0 :
                if self.check_issue(cr, uid, this_obj.student_id.id, this_obj.library_card_id.id, context) == True:
                    if this_obj.book_id.state and this_obj.book_id.state == 'a':
                        book_movement_create = {
                                                'book_id': this_obj.book_id.id,
                                                'quantity': this_obj.quantity,
                                                'type': this_obj.type,
                                                'student_id': this_obj.student_id.id or False,
                                                'faculty_id': this_obj.faculty_id.id or False ,
                                                'library_card_id': this_obj.library_card_id.id,
                                                'issued_date': this_obj.issued_date,
                                                'return_date': this_obj.return_date,
                                                'state': 'i',
                                                }
                        book_move_id = book_movement.create(cr, uid, book_movement_create,context)
                        book.write(cr, uid, this_obj.book_id.id, {'state': 'i'},context)
        
                        value = {'type': 'ir.actions.act_window_close'}
                    else:
                        book_state = this_obj.book_id.state == 'i' and 'Issued' or \
                                      this_obj.book_id.state == 'a' and 'Available' or \
                                      this_obj.book_id.state == 'l' and 'Lost' or \
                                      this_obj.book_id.state == 'r' and 'Reserved'
                        raise osv.except_osv(('Error!'),("Book Can not be issued because book state is : %s") %(book_state))
                else:
                    raise osv.except_osv(('Error!'),("Maximum Number of book allowed for %s is : %s") %(this_obj.student_id.name,this_obj.library_card_id.allow_book))
            else:
                raise osv.except_osv(('Error!'),("There Is No Book Available"))
            
        return value
    


issue_book()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
