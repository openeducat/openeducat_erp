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

import datetime
import pytz
import time
from openerp import models, fields, api, _
from openerp.exceptions import ValidationError

week_number = {
    'Mon': 1,
    'Tue': 2,
    'Wed': 3,
    'Thu': 4,
    'Fri': 5,
    'Sat': 6,
    'Sun': 7,
}


class GenerateTimeTable(models.TransientModel):
    _name = 'generate.time.table'
    _description = 'Generate TimeTables'
    _rec_name = 'course_id'

    course_id = fields.Many2one('op.course', 'Course', required=True)
    batch_id = fields.Many2one('op.batch', 'Batch', required=True)
    time_table_lines = fields.One2many(
        'gen.time.table.line', 'gen_time_table', 'Time Table Lines')
    time_table_lines_1 = fields.One2many(
        'gen.time.table.line', 'gen_time_table', 'Time Table Lines',
        domain=[('day', '=', '1')])
    time_table_lines_2 = fields.One2many(
        'gen.time.table.line', 'gen_time_table', 'Time Table Lines',
        domain=[('day', '=', '2')])
    time_table_lines_3 = fields.One2many(
        'gen.time.table.line', 'gen_time_table', 'Time Table Lines',
        domain=[('day', '=', '3')])
    time_table_lines_4 = fields.One2many(
        'gen.time.table.line', 'gen_time_table', 'Time Table Lines',
        domain=[('day', '=', '4')])
    time_table_lines_5 = fields.One2many(
        'gen.time.table.line', 'gen_time_table', 'Time Table Lines',
        domain=[('day', '=', '5')])
    time_table_lines_6 = fields.One2many(
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
        self.batch_id = False

    @api.one
    def gen_datewise(self, line, st_date, en_date, self_obj):
        day_cnt = 7
        curr_date = st_date
        en_date = en_date.replace(hour=23, minute=59, second=59)
        while curr_date <= en_date:
            hour = line.period_id.hour
            if line.period_id.am_pm == 'pm' and int(hour) != 12:
                hour = int(hour) + 12
            per_time = '%s:%s:00' % (hour, line.period_id.minute)
            local = pytz.timezone(self.env.user.partner_id.tz or 'GMT')
            naive = datetime.datetime.strptime(
                curr_date.strftime('%Y-%m-%d ') +
                per_time, '%Y-%m-%d %H:%M:%S')
            local_dt = local.localize(naive, is_dst=None)
            utc_dt = local_dt.astimezone(pytz.utc)
            utc_dt = utc_dt.strftime("%Y-%m-%d %H:%M:%S")
            curr_date = datetime.datetime.strptime(utc_dt, "%Y-%m-%d %H:%M:%S")
            end_time = datetime.timedelta(hours=line.period_id.duration)
            cu_en_date = curr_date + end_time
            s = fields.Datetime.from_string(self_obj.start_date)
            if curr_date >= s and curr_date <= en_date:
                self.env['op.timetable'].create({
                    'faculty_id': line.faculty_id.id,
                    'subject_id': line.subject_id.id,
                    'course_id': self_obj.course_id.id,
                    'batch_id': self_obj.batch_id.id,
                    'period_id': line.period_id.id,
                    'start_datetime': curr_date.strftime("%Y-%m-%d %H:%M:%S"),
                    'end_datetime': cu_en_date.strftime("%Y-%m-%d %H:%M:%S"),
                    'type': curr_date.strftime('%A'),
                })
            curr_date = curr_date + datetime.timedelta(days=day_cnt)
        return True

    @api.one
    def act_gen_time_table(self):
        st_date = datetime.datetime.strptime(
            self.start_date, '%Y-%m-%d')
        en_date = datetime.datetime.strptime(self.end_date, '%Y-%m-%d')
        st_day = week_number[st_date.strftime('%a')]
        for line in self.time_table_lines:
            if int(line.day) == st_day:
                self.gen_datewise(
                    line, st_date, en_date, self)
            if int(line.day) < st_day:
                new_st_date = st_date - \
                    datetime.timedelta(days=(st_day - int(line.day)))
                self.gen_datewise(
                    line, new_st_date, en_date, self)
            if int(line.day) > st_day:
                new_st_date = st_date + \
                    datetime.timedelta(days=(int(line.day) - st_day))
                self.gen_datewise(
                    line, new_st_date, en_date, self)

        return {'type': 'ir.actions.act_window_close'}


class GenerateTimeTableLine(models.TransientModel):
    _name = 'gen.time.table.line'
    _description = 'Generate Time Table Lines'
    _rec_name = 'day'

    gen_time_table = fields.Many2one(
        'generate.time.table', 'Time Table', required=True)
    faculty_id = fields.Many2one('op.faculty', 'Faculty', required=True)
    subject_id = fields.Many2one('op.subject', 'Subject', required=True)
    day = fields.Selection([
        ('1', 'Monday'),
        ('2', 'Tuesday'),
        ('3', 'Wednesday'),
        ('4', 'Thursday'),
        ('5', 'Friday'),
        ('6', 'Saturday'),
    ], 'Day', required=True)
    period_id = fields.Many2one('op.period', 'Period', required=True)
