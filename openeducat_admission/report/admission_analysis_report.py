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


class ReportAdmissionAnalysis(models.AbstractModel):
    _name = 'report.openeducat_admission.report_admission_analysis'

    def get_total_student(self, data):
        student_search = self.env['op.admission'].search_count(
            [('state', '=', 'done'),
             ('course_id', '=', data['course_id'][0]),
             ('admission_date', '>=', data['start_date']),
             ('admission_date', '<=', data['end_date'])])
        return student_search

    def get_data(self, data):
        lst = []
        student_search = self.env['op.admission'].search(
            [('state', '=', 'done'),
             ('course_id', '=', data['course_id'][0]),
             ('admission_date', '>=', data['start_date']),
             ('admission_date', '<=', data['end_date'])],
            order='admission_date desc')
        res = {}
        self.total_student = 0
        for student in student_search:
            self.total_student += 1
            res = {
                'name': student.name,
                'middle_name': student.middle_name,
                'last_name': student.last_name,
                'application_no': student.application_number,
            }
            lst.append(res)
        return lst

    @api.model
    def get_report_values(self, docids, data=None):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        docargs = {
            'doc_ids': self.ids,
            'doc_model': model,
            'docs': docs,
            'time': time,
            'data': data,
            'start_date': data['start_date'],
            'end_date': data['end_date'],
            'get_total_student': self.get_total_student(data),
            'get_data': self.get_data(data),
        }
        return docargs
