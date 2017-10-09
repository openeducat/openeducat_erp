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

from datetime import datetime
import time

from odoo import models, api


class ReportMarksheetReport(models.AbstractModel):
    _name = 'report.openeducat_exam.report_marksheet_report'

    def get_objects(self, objects):
        obj = []
        for object in objects:
            obj.extend(object)
        return obj

    def get_lines(self, obj):
        lines = []
        for line in obj.marksheet_line:
            lines.extend(line)
        return lines

    def get_date(self, date):
        date1 = datetime.strptime(date, "%Y-%m-%d")
        return str(date1.month) + ' / ' + str(date1.year)

    def get_total(self, marksheet_line):
        total = [x.exam_id.total_marks for x in marksheet_line.result_line]
        return sum(total)

    @api.model
    def get_report_values(self, docids, data=None):
        docs = self.env['op.marksheet.register'].browse(docids)
        docargs = {
            'doc_model': 'op.marksheet.register',
            'docs': docs,
            'time': time,
            'get_objects': self.get_objects,
            'get_lines': self.get_lines,
            'get_date': self.get_date,
            'get_total': self.get_total,
        }
        return docargs
