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

class op_author(osv.osv):
    _name = 'op.student.book.purchase'

    _columns = {
            'name': fields.char(size=128, string='Title', required=True),
            'author_ids': fields.many2one('op.author', string='Author'),
            'edition': fields.text(string='Edition'),
            'publisher_ids': fields.many2one('op.publisher', string='Publisher'),
            'course_ids': fields.many2one('op.course', string='Course'),
            'subject_ids': fields.many2one('op.subject', string='Subject'),
            'student_id': fields.many2one('op.student', string='Student'),
            'faculty_id': fields.many2one('op.faculty', string='Faculty'),
#            'student_id': fields.many2one('op.student', string='Student', required=True, groups="group_op_student"),
#            'faculty_id': fields.many2one('op.faculty', string='Faculty', required=True, groups="group_op_faculty"),
            
            
    }

op_author()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
