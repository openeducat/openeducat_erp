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

import calendar
from datetime import datetime
import time

from odoo import models, api, _


class ReportTimetableStudentGenerate(models.AbstractModel):
    _name = 'report.openeducat_timetable.report_timetable_student_generate'

    def sort_tt(self, data_list):
        main_list = []
        f = []
        for d in data_list:
            if d['period'] not in f:
                f.append(d['period'])
                main_list.append({
                    'name': d['period'],
                    'line': {d['day']: d}
                })
            else:
                for m in main_list:
                    if m['name'] == d['period']:
                        m['line'][d['day']] = d
        return main_list

    def get_heading(self):

        dayofWeek = [_(calendar.day_name[0]),
                     _(calendar.day_name[1]),
                     _(calendar.day_name[2]),
                     _(calendar.day_name[3]),
                     _(calendar.day_name[4]),
                     _(calendar.day_name[5])]
        return dayofWeek

    def get_object(self, data):

        data_list = []
        for timetable_obj in self.env['op.session'].browse(
                data['time_table_ids']):

            oldDate = datetime.strptime(
                timetable_obj.start_datetime, "%Y-%m-%d %H:%M:%S")
            day = datetime.weekday(oldDate)

            timetable_data = {
                'period': timetable_obj.timing_id.name,
                'sequence': timetable_obj.timing_id.sequence,
                'start_datetime': timetable_obj.start_datetime,
                'day': str(day),
                'subject': timetable_obj.subject_id.name,
            }
            data_list.append(timetable_data)
        ttdl = sorted(data_list, key=lambda k: k['sequence'])
        final_list = self.sort_tt(ttdl)
        return final_list

    @api.model
    def render_html(self, docids, data=None):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        docargs = {
            'doc_ids': self.ids,
            'doc_model': model,
            'docs': docs,
            'data': data,
            'time': time,
            'get_object': self.get_object,
            'get_heading': self.get_heading,
        }
        return self.env['report'] \
            .render('openeducat_timetable.report_timetable_student_generate',
                    docargs)
