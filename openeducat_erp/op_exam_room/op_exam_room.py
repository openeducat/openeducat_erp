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

class op_exam_room(osv.osv):
    _name = 'op.exam.room'
    _columns = {
                'name': fields.char('Name', size=256, required=True),
                'classroom_id': fields.many2one('op.classroom', 'Classroom', required=True),
                'capacity': fields.integer(string="Capacity",size=3, required=True),
                'course_ids': fields.many2many('op.course', 'course_exam_room_rel', 'exam_room_id', 'course_id', 'Course'),
                'standard_ids': fields.many2many('op.standard', 'standard_exam_room_rel', 'exam_room_id', 'standard_id', 'Course'),
                'student_ids': fields.many2many('op.student', 'student_exam_room_rel', 'exam_room_id', 'student_id', 'Course'),
    }
    
op_exam_room()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
