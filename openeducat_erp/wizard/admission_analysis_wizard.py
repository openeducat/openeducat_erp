# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
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
###############################################################################

import time

from openerp import models, fields, api


class AdmissionAnalysis(models.TransientModel):

    """ Admission Analysis Wizard """
    _name = 'admission.analysis'

    course_id = fields.Many2one('op.course', 'Course', required=True)
    standard_id = fields.Many2one('op.standard', 'Standard', required=True)
    start_date = fields.Date(
        'Start Date', default=time.strftime('%Y-%m-01'), required=True)
    end_date = fields.Date('End Date', required=True)

    @api.multi
    def print_report(self):
        data = self.read(
            ['course_id', 'standard_id', 'start_date', 'end_date'])[0]
        return self.env['report'].get_action(
            self, 'openeducat_erp.report_admission_analysis', data=data)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
