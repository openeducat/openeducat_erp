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

class op_book_purchase(osv.osv):
    _name = 'op.book.purchase'
    
    
    _columns = {
            'name': fields.char(size=128, string='Title', required=True),
            'author_ids': fields.many2one('op.author', string='Author'),
            'edition': fields.text(string='Edition'),
            'publisher_ids': fields.many2one('op.publisher', string='Publisher'),
            'course_ids': fields.many2one('op.course', string='Course', required=True),
            'subject_ids': fields.many2one('op.subject', string='Subject', required=True),
            'student_id': fields.many2one('op.student', string='Student', groups="openeducat_erp.group_op_student", required=True),
            'faculty_id': fields.many2one('op.faculty', string='Faculty', groups="openeducat_erp.group_op_faculty", required=True),
            'library_id':fields.many2one('res.partner','Librarian', groups="openeducat_erp.group_op_library", required=True),
            'state': fields.selection([('d','Draft'),('rq','Requested'),('a','Accept'),('r','Reject')], string='State', select=True, readonly=True),
            
    }
    
    def get_student(self, cr, uid, *args):
        user_pool = self.pool.get('res.users')
        result = user_pool.browse(cr, uid, uid).user_line
        return result and result[0].id or False
    
    _defaults = {
              'state': 'd',
              'student_id': get_student,
              }

    def act_draft(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'d'})
        return True
    
    def act_requested(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'rq'})
        return True
    
    def act_accept(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'a'})
        return True
    
    def act_reject(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'r'})
        return True


op_book_purchase()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
