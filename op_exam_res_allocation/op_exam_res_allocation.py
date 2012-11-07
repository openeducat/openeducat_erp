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

class op_exam_res_allocation(osv.osv):
    _name = 'op.exam.res.allocation'

    _columns = {
            'exam_session_ids': fields.many2many('op.exam.session','exam_session_rel', 'op_exam', 'op_session', 'Select Exam Session'),
            'exam_ids': fields.many2many('op.exam', 'exam_resource_rel',\
                         'op_exam_id', 'op_resource_id', string='Exam(s)'),
            'faculty_ids': fields.many2many('op.faculty', 'faculty_resource_rel',\
                        'op_faculty_id', 'op_resource_id', string='Faculty'),
            'student_ids': fields.many2many('op.student', 'student_resource_rel',\
                        'op_student_id', 'op_resource_id', string='Student'),
    }

#    def onchange_exam_session_res(self, cr, uid, ids, exam_session_ids, context={}):
#        exams = []
#        students_list = []
#        session_pool = self.pool.get('op.exam.session')
#        for es_id in exam_session_ids[0][2]:
#            exams += [x.id for x in session_pool.browse(cr, uid, es_id, context).exam_ids]
#
#            for exam in session_pool.browse(cr, uid,es_id, context).exam_ids:
#                students_list += [s.id for s in exam.attendees_line]
#        return {
#                'value':{'exam_ids':exams, 'student_ids':students_list}
#                }

    def onchange_exam_session_res(self, cr, uid, ids, exam_session_ids, context={}):
        exams = []
        student_list = []
        session_pool = self.pool.get('op.exam.session')
        student_pool = self.pool.get('op.student')
        
        for session_obj in exam_session_ids[0][2]:
            session_browse = session_pool.browse(cr, uid, session_obj, context)
            student_search = student_pool.search(cr, uid, [('course_id','=',session_browse.course_id.id)])
            for student_obj in student_search:
                student_browse = student_pool.browse(cr, uid, student_obj)
                student_list += [student_browse.id]
                for exam in session_browse.exam_ids:
                    exams += [exam.id]
                return {
                        'value':{'exam_ids':exams, 'student_ids':student_list}
                }
            
op_exam_res_allocation()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
