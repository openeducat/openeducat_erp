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

from openerp import models, fields
from openerp.report import report_sxw


class StudentHallTicketReport(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        super(StudentHallTicketReport, self).__init__(
            cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_data': self.get_data,
        })
        self._context = context

    def get_date(self, exam_line):

        timestamp = fields.Datetime.context_timestamp
        dt = fields.Datetime
        schedule_start = timestamp(self, dt.from_string(exam_line.start_time))
        schedule_end = timestamp(self, dt.from_string(exam_line.end_time))
        schedule_start = fields.Datetime.to_string(schedule_start)
        schedule_end = fields.Datetime.to_string(schedule_end)

        return schedule_start[11:] + ' To ' + schedule_end[11:]

    def get_subject(self, datas):
        lst = []
        for exam_line in datas['exam_ids']:
            res1 = {
                'subject': exam_line.subject_id.name,
                'date': exam_line.start_time[:10],
                'time': self.get_date(exam_line),
                'sup_sign': ''
            }
            lst.append(res1)
        return lst

    def get_data(self, data):
        final_lst = []
        exam_session_pool = self.pool.get('op.exam.session')
        exam_student = self.pool.get('op.student')
        datas = exam_session_pool.browse(
            self.cr, self.uid, data['exam_session_id'][0])
        student_search = exam_student.search(
            self.cr, self.uid, [('course_id', '=', datas.course_id.id)])
        for student in exam_student.browse(self.cr, self.uid, student_search):
            res = {
                'exam': datas.name,
                'exam_code': datas.exam_code,
                'course': datas.course_id.name,
                'student': student.name,
                'photo': student.photo,
                'student_middle': student.middle_name,
                'student_last': student.last_name,
                'roll_number': student.roll_number,
                'line': self.get_subject(datas),
            }
            final_lst.append(res)
        return final_lst


class ReportTicket(models.AbstractModel):
    _name = 'report.openeducat_exam.report_ticket'
    _inherit = 'report.abstract_report'
    _template = 'openeducat_exam.report_ticket'
    _wrapped_report_class = StudentHallTicketReport


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
