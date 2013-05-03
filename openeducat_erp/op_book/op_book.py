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

class op_book(osv.osv):
    _name = 'op.book'

    
    _columns = {
            'name': fields.char(size=128, string='Title', required=True),
            'number_book': fields.integer('No. Of Books', size=256, required=True),
            'id_book': fields.char(size=64, string='ISBN Code'),
            'tag': fields.many2many('op.tag', 'book_tag_rel', 'op_book_id', 'op_tag_id', string='Tag'),
            'author_ids': fields.many2many('op.author', 'book_author_rel', 'op_book_id', 'op_author_id', string='Author', required=True),
            'state': fields.selection([('a','Available'),('i','Issued'),('r','Reserved'),('l','Lost')], string='State'),
            'edition': fields.text(string='Edition'),
            'publisher_ids': fields.many2many('op.publisher', 'book_publisher_rel', 'op_book_id', 'op_publisher_id', string='Publisher', required=True),
            'course_ids': fields.many2many('op.course', 'book_course_rel', 'op_book_id', 'op_course_id', string='Course', required=True),
            'movement_line': fields.one2many('op.book.movement', 'book_id', string='Movement'),
            'subject_ids': fields.many2many('op.subject', 'book_subject_rel', 'op_book_id', 'op_subject_id', string='Subjects', required=True),
            'internal_code': fields.char(size=64, string='Internal ID'),
            'queue_ids': fields.many2many('op.book.queue', 'op_queue_book_rl', 'op_queue_id', 'op_book_id', 'Book Queue'),
    }

    def do_return(self, cr, uid, ids, context={}):
        value = {}
        data_obj = self.pool.get('ir.model.data')
        search_view_id = data_obj._get_id(cr, uid, 'openeducat_erp', 'view_op_book_movement_search')
        search_id = data_obj.read(cr, uid, search_view_id, ['res_id'])
        book_move_pool = self.pool.get('op.book.movement')
        book_search_issue = book_move_pool.search(cr, uid, [('book_id','=',ids[0]),('state','=','i')])
        value = {
                'name': _('Book Return'),
                'domain': [('id','in',book_search_issue)],
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'op.book.movement',
                'view_id': False,
                'search_view_id':search_id['res_id'],
                'res_id': book_search_issue,
#                'views': [('form', form_id),('tree', tree_id)],
                'type': 'ir.actions.act_window',
                'target':'new',
                }
        return value
    
    _defaults={
               'state': 'a'
               }

op_book()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
