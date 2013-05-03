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

class op_all_student_wizard(osv.osv_memory):

    _name = 'op.all.student'

    _columns = {
                'student_ids': fields.many2many('op.student', 'student_student_rel', 'op_student_id', 'student_id', string='Add Student(s)'),
                }

    def confirm_student(self, cr, uid, ids, context={}):
        value = {}
        student_pool = self.pool.get("op.student")
        sheet_pool = self.pool.get('op.attendance.sheet')
        data = self.read(cr, uid, ids)[0]


        data.update({'ids':context.get('active_ids',[]), 'student_ids': data['student_ids']})

        for sheet in context.get('active_ids',[]):
            sheet_browse = sheet_pool.browse(cr, uid, sheet)
            course = sheet_browse.register_id.course_id.id
            standard = sheet_browse.register_id.standard_id.id
            division = sheet_browse.register_id.division_id.id
            absent_list = [x.student_id.id for x in sheet_browse.attendance_line]
            all_student_search = student_pool.search(cr, uid, [('course_id','=',course),
                                                               ('standard_id','=',standard),
                                                               ('division_id','=',division),
                                                               '|',('course_id','=',course),
                                                               ('standard_id','=',standard)])
            
            all_student_search = list(set(all_student_search)-set(absent_list))
            for student_data in all_student_search:
                dic = {}
                student = student_pool.browse(cr,uid, student_data)
                if student.id in data['student_ids']:
                    dic = {
                           'student_id':student.id,
                           'absent':False,
                           'attendance_id': context.get('active_id'),
                           }
                else:
                    dic = {
                           'student_id':student.id,
                           'present':True,
                           'attendance_id': context.get('active_id'),
                           }
                cr_id = self.pool.get('op.attendance.line').create(cr, uid, dic, context=context)
            value = {'type': 'ir.actions.act_window_close'}
            return value

op_all_student_wizard()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
