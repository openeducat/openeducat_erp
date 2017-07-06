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
import datetime
import pytz
import time

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class GenerateSession(models.TransientModel):
    _name = 'generate.time.table'
    _description = 'Generate Sessions'
    _rec_name = 'course_id'

    course_id = fields.Many2one('op.course', 'Course', required=True)
    batch_id = fields.Many2one('op.batch', 'Batch', required=True)
    time_table_lines = fields.One2many(
        'gen.time.table.line', 'gen_time_table', 'Time Table Lines')
    time_table_lines_1 = fields.One2many(
        'gen.time.table.line', 'gen_time_table', 'Time Table Lines',
        domain=[('day', '=', '0')])
    time_table_lines_2 = fields.One2many(
        'gen.time.table.line', 'gen_time_table', 'Time Table Lines',
        domain=[('day', '=', '1')])
    time_table_lines_3 = fields.One2many(
        'gen.time.table.line', 'gen_time_table', 'Time Table Lines',
        domain=[('day', '=', '2')])
    time_table_lines_4 = fields.One2many(
        'gen.time.table.line', 'gen_time_table', 'Time Table Lines',
        domain=[('day', '=', '3')])
    time_table_lines_5 = fields.One2many(
        'gen.time.table.line', 'gen_time_table', 'Time Table Lines',
        domain=[('day', '=', '4')])
    time_table_lines_6 = fields.One2many(
        'gen.time.table.line', 'gen_time_table', 'Time Table Lines',
        domain=[('day', '=', '5')])
    time_table_lines_7 = fields.One2many(
        'gen.time.table.line', 'gen_time_table', 'Time Table Lines',
        domain=[('day', '=', '6')])
    start_date = fields.Date(
        'Start Date', required=True, default=time.strftime('%Y-%m-01'))
    end_date = fields.Date('End Date', required=True)

    @api.constrains('start_date', 'end_date')
    def check_dates(self):
        start_date = fields.Date.from_string(self.start_date)
        end_date = fields.Date.from_string(self.end_date)
        if start_date > end_date:
            raise ValidationError(_("End Date cannot be set before \
            Start Date."))

    @api.onchange('course_id')
    def onchange_course(self):
        if self.batch_id and self.course_id:
            if self.batch_id.course_id != self.course_id:
                self.batch_id = False

    @api.multi
    def act_gen_time_table(self):
        for session in self:
            start_date = datetime.datetime.strptime(
                session.start_date, '%Y-%m-%d')
            end_date = datetime.datetime.strptime(session.end_date, '%Y-%m-%d')

            for n in range((end_date - start_date).days + 1):
                curr_date = start_date + datetime.timedelta(n)
                for line in session.time_table_lines:
                    if int(line.day) == curr_date.weekday():
                        hour = line.timing_id.hour
                        if line.timing_id.am_pm == 'pm' and int(hour) != 12:
                            hour = int(hour) + 12
                        per_time = '%s:%s:00' % (hour, line.timing_id.minute)
                        final_date = datetime.datetime.strptime(
                            curr_date.strftime('%Y-%m-%d ') +
                            per_time, '%Y-%m-%d %H:%M:%S')
                        local_tz = pytz.timezone(
                            self.env.user.partner_id.tz or 'GMT')
                        local_dt = local_tz.localize(final_date, is_dst=None)
                        utc_dt = local_dt.astimezone(pytz.utc)
                        utc_dt = utc_dt.strftime("%Y-%m-%d %H:%M:%S")
                        curr_start_date = datetime.datetime.strptime(
                            utc_dt, "%Y-%m-%d %H:%M:%S")
                        curr_end_date = curr_start_date + datetime.timedelta(
                            hours=line.timing_id.duration)
                        self.env['op.session'].create({
                            'faculty_id': line.faculty_id.id,
                            'subject_id': line.subject_id.id,
                            'course_id': session.course_id.id,
                            'batch_id': session.batch_id.id,
                            'timing_id': line.timing_id.id,
                            'classroom_id': line.classroom_id.id,
                            'start_datetime':
                            curr_start_date.strftime("%Y-%m-%d %H:%M:%S"),
                            'end_datetime':
                            curr_end_date.strftime("%Y-%m-%d %H:%M:%S"),
                            'type': calendar.day_name[int(line.day)],
                        })
            return {'type': 'ir.actions.act_window_close'}


class GenerateSessionLine(models.TransientModel):
    _name = 'gen.time.table.line'
    _description = 'Generate Time Table Lines'
    _rec_name = 'day'

    gen_time_table = fields.Many2one(
        'generate.time.table', 'Time Table', required=True)
    faculty_id = fields.Many2one('op.faculty', 'Faculty', required=True)
    subject_id = fields.Many2one('op.subject', 'Subject', required=True)
    timing_id = fields.Many2one('op.timing', 'Timing', required=True)
    classroom_id = fields.Many2one('op.classroom', 'Classroom')
    day = fields.Selection([
        ('0', calendar.day_name[0]),
        ('1', calendar.day_name[1]),
        ('2', calendar.day_name[2]),
        ('3', calendar.day_name[3]),
        ('4', calendar.day_name[4]),
        ('5', calendar.day_name[5]),
        ('6', calendar.day_name[6]),
    ], 'Day', required=True)
