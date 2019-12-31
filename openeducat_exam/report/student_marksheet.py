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
from odoo import models, api, fields


class ReportMarksheetReport(models.AbstractModel):
    _name = "report.openeducat_exam.report_marksheet_report"
    _description = "Exam Marksheet Report"

    def get_objects(self, objects):
        obj = []
        for data in objects:
            obj.extend(data)
        return obj

    def get_lines(self, obj):
        lines = []
        for line in obj.result_line:
            lines.extend(line)
        return lines

    def get_date(self, date):
        date1 = fields.Date.to_date(date)
        return str(date1.month) + ' / ' + str(date1.year)

    def get_total(self, result_line):
        total = [x.exam_id.total_marks for x in result_line]
        return sum(total)

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['op.marksheet.line'].browse(docids)
        docargs = {
            'doc_model': 'op.marksheet.line',
            'docs': docs,
            'time': time,
            'get_objects': self.get_objects,
            'get_lines': self.get_lines,
            'get_date': self.get_date,
            'get_total': self.get_total,
        }
        return docargs
