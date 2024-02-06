# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<https://www.openeducat.org>).
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
from odoo import models, fields, _
from odoo.exceptions import ValidationError


class AdmissionAnalysis(models.TransientModel):
    """ Admission Analysis Wizard """
    _name = "admission.analysis"
    _description = "Admission Analysis Wizard"

    course_id = fields.Many2one('op.course', 'Course', required=True)
    start_date = fields.Date(
        'Start Date', default=time.strftime('%Y-%m-01'), required=True)
    end_date = fields.Date('End Date', required=True)

    def print_report(self):
        start_date = fields.Date.from_string(self.start_date)
        end_date = fields.Date.from_string(self.end_date)
        if start_date > end_date:
            raise ValidationError(
                _("End Date cannot be set before Start Date."))
        else:
            data = self.read(
                ['course_id', 'start_date', 'end_date'])[0]
            report = self.env.ref(
                'openeducat_admission.action_report_report_admission_analysis'
            )
            return report.report_action(self, data=data)
