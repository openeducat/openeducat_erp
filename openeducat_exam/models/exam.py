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

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class OpExam(models.Model):
    _name = "op.exam"
    _inherit = "mail.thread"
    _description = "Exam"

    session_id = fields.Many2one('op.exam.session', 'Exam Session')
    course_id = fields.Many2one(
        'op.course', related='session_id.course_id', store=True,
        readonly=True)
    batch_id = fields.Many2one(
        'op.batch', 'Batch', related='session_id.batch_id', store=True,
        readonly=True)
    subject_id = fields.Many2one('op.subject', 'Subject', required=True)
    exam_code = fields.Char('Exam Code', size=16, required=True)
    attendees_line = fields.One2many(
        'op.exam.attendees', 'exam_id', 'Attendees', readonly=True)
    start_time = fields.Datetime('Start Time', required=True)
    end_time = fields.Datetime('End Time', required=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('schedule', 'Scheduled'), ('held', 'Held'),
         ('result_updated', 'Result Updated'),
         ('cancel', 'Cancelled'), ('done', 'Done')], 'State',
        readonly=True, default='draft', track_visibility='onchange')
    note = fields.Text('Note')
    responsible_id = fields.Many2many('op.faculty', string='Responsible')
    name = fields.Char('Exam', size=256, required=True)
    total_marks = fields.Integer('Total Marks', required=True)
    min_marks = fields.Integer('Passing Marks', required=True)

    _sql_constraints = [
        ('unique_exam_code',
         'unique(exam_code)', 'Code should be unique per exam!')]

    @api.constrains('total_marks', 'min_marks')
    def _check_marks(self):
        if self.total_marks <= 0.0 or self.min_marks <= 0.0:
            raise ValidationError(_('Enter proper marks!'))
        if self.min_marks > self.total_marks:
            raise ValidationError(_(
                "Passing Marks can't be greater than Total Marks"))

    @api.constrains('start_time', 'end_time')
    def _check_date_time(self):
        session_start = datetime.datetime.combine(
            fields.Date.from_string(self.session_id.start_date),
            datetime.time.min)
        session_end = datetime.datetime.combine(
            fields.Date.from_string(self.session_id.end_date),
            datetime.time.max)
        start_time = fields.Datetime.from_string(self.start_time)
        end_time = fields.Datetime.from_string(self.end_time)
        if start_time > end_time:
            raise ValidationError(_('End Time cannot be set \
            before Start Time.'))
        elif start_time < session_start or start_time > session_end or \
                end_time < session_start or end_time > session_end:
            raise ValidationError(
                _('Exam Time should in between Exam Session Dates.'))

    @api.multi
    def act_result_updated(self):
        self.state = 'result_updated'

    @api.multi
    def act_done(self):
        self.state = 'done'

    @api.multi
    def act_draft(self):
        self.state = 'draft'

    @api.multi
    def act_cancel(self):
        self.state = 'cancel'
