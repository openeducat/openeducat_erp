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

from openerp import models, fields, api
from openerp.exceptions import ValidationError


class OpExam(models.Model):
    _name = 'op.exam'
    _inherit = 'mail.thread'
    _description = 'Exam'

    session_id = fields.Many2one('op.exam.session', 'Exam Session')
    subject_id = fields.Many2one('op.subject', 'Subject', required=True)
    exam_code = fields.Char('Exam Code', size=8, required=True)
    exam_type = fields.Many2one('op.exam.type', 'Exam Type', required=True)
    evaluation_type = fields.Selection(
        [('normal', 'Normal'), ('GPA', 'GPA'), ('CWA', 'CWA'), ('CCE', 'CCE')],
        'Evaluation Type', default="normal", required=True)
    attendees_line = fields.One2many(
        'op.exam.attendees', 'exam_id', 'Attendees', readonly=True)
    venue = fields.Many2one('res.partner', 'Venue')
    start_time = fields.Datetime('Start Time', required=True)
    end_time = fields.Datetime('End Time', required=True)
    state = fields.Selection(
        [('new', 'New Exam'), ('schedule', 'Scheduled'), ('held', 'Held'),
         ('cancel', 'Cancelled'), ('done', 'Done')], 'State', select=True,
        readonly=True, default='new', track_visibility='onchange')
    note = fields.Text('Note')
    responsible_id = fields.Many2many('op.faculty', string='Responsible')
    name = fields.Char('Exam', size=256, required=True)
    total_marks = fields.Float('Total Marks', required=True)
    min_marks = fields.Float('Passing Marks', required=True)

    @api.constrains('total_marks', 'min_marks')
    def _check_marks(self):
        if self.total_marks <= 0.0 or self.min_marks <= 0.0:
            raise ValidationError('Enter proper marks!')
        if self.min_marks > self.total_marks:
            raise ValidationError(
                "Passing Marks can't be greater than Total Marks")

    @api.constrains('start_time', 'end_time')
    def _check_date_time(self):
        if self.start_time > self.end_time:
            raise ValidationError('End Time cannot be set before Start Time.')

    @api.one
    def act_held(self):
        self.state = 'held'

    @api.one
    def act_done(self):
        self.state = 'done'

    @api.one
    def act_schedule(self):
        self.state = 'schedule'

    @api.one
    def act_cancel(self):
        self.state = 'cancel'

    @api.one
    def act_new_exam(self):
        self.state = 'new'


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
