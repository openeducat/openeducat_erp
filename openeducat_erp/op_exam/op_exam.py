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

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class OpExamSession(models.Model):
    _name = 'op.exam.session'
    _description = 'Exam Session'

    name = fields.Char('Exam', size=256, required=True)
    course_id = fields.Many2one('op.course', 'Course', required=True)
    batch_id = fields.Many2one('op.batch', 'Batch', required=True)
    standard_id = fields.Many2one('op.standard', 'Standard', required=True)
    division_id = fields.Many2one('op.division', 'Division')
    exam_code = fields.Char('Exam Code', size=8, required=True)
    start_time = fields.Datetime('Start Time', required=True)
    end_time = fields.Datetime('End Time', required=True)
    room_id = fields.Many2one('op.exam.room', 'Room', required=True)
    exam_ids = fields.One2many('op.exam', 'session_id', 'Exams')

    @api.constrains('start_time', 'end_time')
    def _check_date_time(self):
        if self.start_time > self.end_time:
            raise ValidationError(
                _('Start Time Should be greater than End Time.'))


class OpExam(models.Model):
    _name = 'op.exam'

    session_id = fields.Many2one('op.exam.session', 'Exam Session')
    subject_id = fields.Many2one('op.subject', 'Subject', required=True)
    division_id = fields.Many2one('op.division', 'Division')
    exam_code = fields.Char('Exam Code', size=8, required=True)
    exam_type = fields.Many2one('op.exam.type', 'Exam Type', required=True)
    evaluation_type = fields.Selection(
        [('normal', 'Normal'), ('GPA', 'GPA'), ('CWA', 'CWA'), ('CCE', 'CCE')],
        'Evaluation Type', required=True)
    attendees_line = fields.One2many(
        'op.exam.attendees', 'exam_id', 'Attendees', required=True)
    venue = fields.Many2one('res.partner', 'Venue')
    start_time = fields.Datetime('Start Time', required=True)
    end_time = fields.Datetime('End Time', required=True)
    state = fields.Selection(
        [('n', 'New Exam'), ('h', 'Held'), ('s', 'Scheduled'), ('d', 'Done'),
         ('c', 'Cancelled')], 'State', select=True, readonly=True, default='n')
    note = fields.Text('Note')
    responsible_id = fields.Many2many('op.faculty', string='Responsible')
    name = fields.Char('Exam', size=256, required=True)
    total_marks = fields.Float('Total Marks')
    min_marks = fields.Float('Passing Marks')

    @api.constrains('start_time', 'end_time')
    def _check_date_time(self):
        if self.start_time > self.end_time:
            raise ValidationError(
                _('Start Time Should be greater than End Time.'))

    @api.one
    def act_held(self):
        self.state = 'h'

    @api.one
    def act_done(self):
        self.state = 'd'

    @api.one
    def act_schedule(self):
        self.state = 's'

    @api.one
    def act_cancel(self):
        self.state = 'c'

    @api.one
    def act_new_exam(self):
        self.state = 'n'

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
