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


class TimeTableReport(models.TransientModel):
    _name = 'time.table.report'
    _description = 'Generate Time Table Report'

    standard_id = fields.Many2one('op.standard', 'Standard')
    division_id = fields.Many2one('op.division', 'Division')
    faculty_id = fields.Many2one('op.faculty', 'Faculty')
    start_date = fields.Date(
        'Start Date', required=True, default=time.strftime('%Y-%m-01'))
    end_date = fields.Date(
        'End Date', required=True)
    state = fields.Selection(
        [('s', 'Student'), ('t', 'Teacher')], string='Select', required=True,
        default='t')

    @api.multi
    def gen_time_table_report(self):
        data = self.read(
            ['start_date', 'end_date', 'standard_id', 'division_id', 'state',
             'faculty_id'])[0]
        if data['state'] == 's':
            time_table_ids = self.env['op.timetable'].search(
                [('standard_id', '=', data['standard_id'][0]),
                 ('division_id', '=', data['division_id'][0]),
                 ('start_datetime', '>', data['start_date'] + '%H:%M:%S'),
                 ('end_datetime', '<', data['end_date'] + '%H:%M:%S')],
                order='start_datetime asc')

            data.update({'time_table_ids': time_table_ids.ids})
            return self.env['report'].get_action(
                self, 'openeducat_erp.report_time_table_student_generate',
                data=data)
        else:
            teacher_time_table_ids = self.env['op.timetable'].search(
                [('start_datetime', '>', data['start_date'] + '%H:%M:%S'),
                 ('end_datetime', '<', data['end_date'] + '%H:%M:%S'),
                 ('faculty_id', '=', data['faculty_id'][0])],
                order='start_datetime asc')

            data.update({'teacher_time_table_ids': teacher_time_table_ids.ids})
            return self.env['report'].get_action(
                self, 'openeducat_erp.report_time_table_teacher_generate',
                data=data)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
