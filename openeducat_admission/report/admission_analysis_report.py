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


class AdmissionAnalysisReport(report_sxw.rml_parse):

    _name = 'report.openeducat_admission.admission_analysis_report'

    def __init__(self, cr, uid, name, context=None):
        super(AdmissionAnalysisReport, self).__init__(
            cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_data': self.get_data,
            'get_total_student': self.get_total_student,
        })

    def get_total_student(self, data):
        return self.total_student

    def get_data(self, data):
        lst = []
        student_pool = self.pool.get('op.admission')
        student_search = student_pool.search(
            self.cr, self.uid, [('state', '=', 'done'),
                                ('course_id', '=', data['course_id'][0]),
                                ('admission_date', '>=', data['start_date']),
                                ('admission_date', '<=', data['end_date'])],
            order='admission_date desc')
        res = {}
        self.total_student = 0
        for student in student_pool.browse(self.cr, self.uid, student_search):
            self.total_student += 1
            res = {
                'name': student.name,
                'middle_name': student.middle_name,
                'last_name': student.last_name,
                'application_no': student.application_number,
            }
            lst.append(res)
        return lst


class ReportAdmissionAnalysis(models.AbstractModel):
    _name = 'report.openeducat_admission.report_admission_analysis'
    _inherit = 'report.abstract_report'
    _template = 'openeducat_admission.report_admission_analysis'
    _wrapped_report_class = AdmissionAnalysisReport


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
