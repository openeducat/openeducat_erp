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

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
week_days = [(calendar.day_name[0], calendar.day_name[0]),
             (calendar.day_name[1], calendar.day_name[1]),
             (calendar.day_name[2], calendar.day_name[2]),
             (calendar.day_name[3], calendar.day_name[3]),
             (calendar.day_name[4], calendar.day_name[4]),
             (calendar.day_name[5], calendar.day_name[5]),
             (calendar.day_name[6], calendar.day_name[6])]


class OpTimetable(models.Model):
    _name = 'op.timetable'
    _inherit = ['mail.thread']
    _description = 'TimeTables'
    _rec_name = 'faculty_id'

    period_id = fields.Many2one(
        'op.period', 'Period', required=True, track_visibility="onchange")
    start_datetime = fields.Datetime(
        'Start Time', required=True,
        default=lambda self: fields.Datetime.now(),
        track_visibility="onchange")
    end_datetime = fields.Datetime(
        'End Time', required=True, track_visibility="onchange")
    course_id = fields.Many2one(
        'op.course', 'Course', required=True, track_visibility="onchange")
    faculty_id = fields.Many2one(
        'op.faculty', 'Faculty', required=True, track_visibility="onchange")
    batch_id = fields.Many2one(
        'op.batch', 'Batch', required=True, track_visibility="onchange")
    subject_id = fields.Many2one(
        'op.subject', 'Subject', required=True, track_visibility="onchange")
    classroom_id = fields.Many2one(
        'op.classroom', 'Classroom', track_visibility='onchange')
    color = fields.Integer('Color Index')
    type = fields.Selection(week_days, 'Days', track_visibility="onchange")
    state = fields.Selection(
        [('draft', 'Draft'), ('done', 'Done'), ('cancel', 'Canceled')],
        'Status', default='draft')
    user_ids = fields.Many2many(
        'res.users', compute='_compute_batch_users',
        store=True, string='Users')

    # For record rule on student and faculty dashboard
    @api.one
    @api.depends('batch_id', 'faculty_id')
    def _compute_batch_users(self):
        usr = []
        students = self.env['op.student'].search(
            [('course_detail_ids.batch_id', '=', self.batch_id.id)])
        for x in students:
            if x.user_id:
                usr.append(x.user_id.id)
        if self.faculty_id.user_id:
            usr.append(self.faculty_id.user_id.id)
        self.user_ids = usr

    @api.one
    def lecture_done(self):
        self.state = 'done'

    @api.one
    def lecture_cancel(self):
        self.state = 'cancel'

    @api.constrains('start_datetime', 'end_datetime')
    def _check_date_time(self):
        if self.start_datetime > self.end_datetime:
            raise ValidationError(_(
                'End Time cannot be set before Start Time.'))

    @api.onchange('course_id')
    def onchange_course(self):
        self.batch_id = False

    @api.onchange('start_datetime')
    def onchange_start_date(self):
        start_datetime = datetime.datetime.strptime(
            self.start_datetime, "%Y-%m-%d %H:%M:%S")
        if start_datetime and start_datetime.weekday() == 0:
            self.type = calendar.day_name[0]
        elif start_datetime and start_datetime.weekday() == 1:
            self.type = calendar.day_name[1]
        elif start_datetime and start_datetime.weekday() == 2:
            self.type = calendar.day_name[2]
        elif start_datetime and start_datetime.weekday() == 3:
            self.type = calendar.day_name[3]
        elif start_datetime and start_datetime.weekday() == 4:
            self.type = calendar.day_name[4]
        elif start_datetime and start_datetime.weekday() == 5:
            self.type = calendar.day_name[5]
