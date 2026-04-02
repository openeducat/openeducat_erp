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

from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SessionReport(models.TransientModel):
    _name = "time.table.report"
    _description = "Generate Time Table Report"

    state = fields.Selection(
        [('faculty', 'Faculty'), ('student', 'Student')],
        string='Select', required=True, default='faculty')
    course_id = fields.Many2one('op.course', 'Course')
    batch_id = fields.Many2one('op.batch', 'Batch')
    faculty_id = fields.Many2one('op.faculty', 'Faculty')
    start_date = fields.Date(
        'Start Date', required=True,
        default=(datetime.today() - relativedelta(
            days=datetime.date(
                datetime.today()).weekday())).strftime('%Y-%m-%d'))
    end_date = fields.Date(
        'End Date', required=True,
        default=(datetime.today() + relativedelta(days=6 - datetime.date(
            datetime.today()).weekday())).strftime('%Y-%m-%d'))

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for session in self:
            start_date = fields.Date.from_string(session.start_date)
            end_date = fields.Date.from_string(session.end_date)
            if end_date < start_date:
                raise ValidationError(_('End Date cannot be set before \
                Start Date.'))
            elif end_date > (start_date + timedelta(days=6)):
                raise ValidationError(_("Select date range for a week!"))

    @api.onchange('course_id')
    def onchange_course(self):
        if self.batch_id and self.course_id:
            if self.batch_id.course_id != self.course_id:
                self.batch_id = False

    def gen_time_table_report(self):
        self.ensure_one()
        template = self.env.ref(
            'openeducat_timetable.report_teacher_timetable_generate')
        data = self.read(
            ['start_date', 'end_date', 'course_id', 'batch_id', 'state',
             'faculty_id'])[0]
        if self.state == 'student':
            domain = [
                ('start_datetime', '>=', self.start_date),
                ('end_datetime', '<=', self.end_date)
            ]
            if self.course_id:
                domain.append(('course_id', '=', self.course_id.id))
            if self.batch_id:
                domain.append(('batch_id', '=', self.batch_id.id))
                
            time_table_ids = self.env['op.session'].search(
                domain, order='start_datetime asc')
            data.update({'time_table_ids': time_table_ids.ids})
            template = self.env.ref(
                'openeducat_timetable.report_student_timetable_generate')
        else:
            domain = [
                ('start_datetime', '>=', self.start_date),
                ('end_datetime', '<=', self.end_date)
            ]
            if self.faculty_id:
                domain.append(('faculty_id', '=', self.faculty_id.id))
                
            teacher_time_table_ids = self.env['op.session'].search(
                domain, order='start_datetime asc')
            data.update({'teacher_time_table_ids': teacher_time_table_ids.ids})
        return template.report_action(self, data=data)
