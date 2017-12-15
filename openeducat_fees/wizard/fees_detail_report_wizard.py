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

from odoo import models, fields, api


class FeesDetailReportWizard(models.TransientModel):

    """ Admission Analysis Wizard """
    _name = 'fees.detail.report.wizard'

    fees_filter = fields.Selection(
        [('student', 'Student'), ('course', 'Course')], 'Fees Filter',
        required=True)
    student_id = fields.Many2one('op.student', 'Student')
    course_id = fields.Many2one('op.course', 'Course')

    @api.multi
    def print_report(self):
        data = {}
        if self.fees_filter == 'student':
            data['fees_filter'] = self.fees_filter
            data['student'] = self.student_id.id
        else:
            data['fees_filter'] = self.fees_filter
            data['course'] = self.course_id.id

        report = self.env.ref(
            'openeducat_fees.action_report_fees_detail_analysis')
        return report.report_action(self, data=data)
