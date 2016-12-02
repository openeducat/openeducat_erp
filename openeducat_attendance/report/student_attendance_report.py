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

from odoo import models, api


class StudentAttendanceReport(models.AbstractModel):

    _name = 'report.openeducat_attendance.student_attendance_report'

    def get_student_name(self, data):
        student = self.env['op.student'].browse(data['student_id'])
        if student:
            return ' '.join([student.name,
                             student.middle_name,
                             student.last_name])

    def get_data(self, data):

        sheet_search = self.env['op.attendance.sheet'].search(
            [('attendance_date', '>=', data['from_date']),
             ('attendance_date', '<=', data['to_date'])],
            order='attendance_date asc')

        lst = []
        for sheet in sheet_search:
            for line in sheet.attendance_line:
                dic = {}
                if data['student_id'] == line.student_id.id and \
                        not line.present:
                    dic = {
                        'absent_date': sheet.attendance_date,
                        'remark': line.remark
                    }
                    lst.append(dic)
        return [{'total': len(lst),
                 'line': lst}]

    @api.model
    def render_html(self, docids, data=None):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        docargs = {
            'doc_ids': self.ids,
            'doc_model': model,
            'docs': docs,
            'time': time,
            'from_date': data['from_date'],
            'to_date': data['to_date'],
            'get_student_name': self.get_student_name(data),
            'get_data': self.get_data(data),
        }
        return self.env['report'] \
            .render('openeducat_attendance.student_attendance_report', docargs)
