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

from odoo import models, fields, api


class ReportTicket(models.AbstractModel):
    _name = 'report.openeducat_exam.report_ticket'

    def get_date(self, exam_line):
        timestamp = fields.Datetime.context_timestamp
        dt = fields.Datetime
        schedule_start = timestamp(self, dt.from_string(exam_line.start_time))
        schedule_end = timestamp(self, dt.from_string(exam_line.end_time))
        schedule_start = fields.Datetime.to_string(schedule_start)
        schedule_end = fields.Datetime.to_string(schedule_end)

        return schedule_start[11:] + ' To ' + schedule_end[11:]

    def get_subject(self, exam_session):
        lst = []
        for exam_line in exam_session['exam_ids']:
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
        exam_session = self.env['op.exam.session'].browse(
            data['exam_session_id'][0])
        student_search = self.env['op.student'].search(
            [('course_detail_ids.course_id', '=', exam_session.course_id.id)])
        for student in student_search:
            student_course = self.env['op.student.course'].search(
                [('student_id', '=', student.id),
                 ('course_id', '=', exam_session.course_id.id)])
            res = {
                'exam': exam_session.name,
                'exam_code': exam_session.exam_code,
                'course': exam_session.course_id.name,
                'student': student.name,
                'photo': student.photo,
                'student_middle': student.middle_name,
                'student_last': student.last_name,
                'roll_number': student_course.roll_number,
                'line': self.get_subject(exam_session),
            }
            final_lst.append(res)
        return final_lst

    @api.model
    def render_html(self, docids, data=None):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        docargs = {
            'doc_ids': self.ids,
            'doc_model': model,
            'docs': docs,
            'time': time,
            'get_data': self.get_data(data),
        }
        return self.env['report'] \
            .render('openeducat_exam.report_ticket', docargs)
