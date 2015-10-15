# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import time
from openerp import models
from openerp.report import report_sxw


class ExamStudentLableReport(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        super(ExamStudentLableReport, self).__init__(
            cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_student_data': self.get_student_data
        })

    def format_list(self, temp_list):
        cnt = 1
        temp = {}
        lst = []
        for i in temp_list:
            if cnt <= 3:
                temp.update({str(cnt): i})
                cnt += 1
            else:
                cnt = 1
                lst.append(temp)
                temp = {}
                temp.update({str(cnt): i})
                cnt += 1
        index = len(temp_list) - len(temp_list) % 3
        if len(temp_list) % 3 == 1:
            lst.append({'1': temp_list[index]})
        elif len(temp_list) % 3 == 2:
            lst.append({'1': temp_list[index], '2': temp_list[index + 1]})
        else:
            lst.append(
                {'1': temp_list[-3], '2': temp_list[-2], '3': temp_list[-1]})
        return lst

    def get_student_data(self, exam_session_ids):

        student_pool = self.pool.get('op.student')
        ret_list = []
        for line in exam_session_ids:
            student_ids = student_pool.search(
                self.cr, self.uid, [('course_id', '=', line.course_id.id),
                                    ], order='id asc')

            temp_list = []
            for student in student_pool.browse(self.cr, self.uid, student_ids):
                res = {
                    'student': student.name,
                    'middle_name': student.middle_name,
                    'last_name': student.last_name,
                    'course': student.course_id.name,
                    'roll_number': student.roll_number,
                }
                temp_list.append(res)
            ret_list.append({'course': line.course_id.name,
                             'line': self.format_list(temp_list)})
        return ret_list


class ReportExamStudentLable(models.AbstractModel):
    _name = 'report.openeducat_exam.report_exam_student_lable'
    _inherit = 'report.abstract_report'
    _template = 'openeducat_exam.report_exam_student_lable'
    _wrapped_report_class = ExamStudentLableReport


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
