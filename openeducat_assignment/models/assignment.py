# -*- coding: utf-8 -*-
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

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class GradingAssigment(models.Model):
    _name = 'grading.assignment'
    _description = "Grading Assignment"

    name = fields.Char('Name', required=True)
    course_id = fields.Many2one('op.course', 'Course', required=True)
    subject_id = fields.Many2one('op.subject', string='Subject')
    issued_date = fields.Datetime('Issued Date', required=True)
    assignment_type = fields.Many2one('grading.assignment.type',
                                      string='Assignment Type', required=True)
    faculty_id = fields.Many2one(
        'op.faculty', 'Faculty', default=lambda self: self.env[
            'op.faculty'].search([('user_id', '=', self.env.uid)]),
        required=True)
    point = fields.Float('Points')


class OpAssignment(models.Model):
    _name = "op.assignment"
    _inherit = "mail.thread"
    _description = "Assignment"
    _order = "submission_date DESC"
    _inherits = {"grading.assignment": "grading_assignment_id"}

    batch_id = fields.Many2one('op.batch', 'Batch', required=True)
    marks = fields.Float('Marks', tracking=True)
    description = fields.Text('Description', required=True)
    state = fields.Selection([
        ('draft', 'Draft'), ('publish', 'Published'),
        ('finish', 'Finished'), ('cancel', 'Cancel'),
    ], 'State', required=True, default='draft', tracking=True)
    submission_date = fields.Datetime('Submission Date', required=True,
                                      tracking=True)
    allocation_ids = fields.Many2many('op.student', string='Allocated To')
    assignment_sub_line = fields.One2many('op.assignment.sub.line',
                                          'assignment_id', 'Submissions')
    reviewer = fields.Many2one('op.faculty', 'Reviewer')
    active = fields.Boolean(default=True)
    grading_assignment_id = fields.Many2one('grading.assignment', 'Grading Assignment',
                                            required=True, ondelete="cascade")

    @api.constrains('issued_date', 'submission_date')
    def check_dates(self):
        for record in self:
            issued_date = fields.Date.from_string(record.issued_date)
            submission_date = fields.Date.from_string(record.submission_date)
            if issued_date > submission_date:
                raise ValidationError(_(
                    "Submission Date cannot be set before Issue Date."))

    @api.onchange('course_id')
    def onchange_course(self):
        self.batch_id = False
        if self.course_id:
            subject_ids = self.env['op.course'].search([
                ('id', '=', self.course_id.id)]).subject_ids
            return {'domain': {'subject_id': [('id', 'in', subject_ids.ids)]}}

    def act_publish(self):
        result = self.state = 'publish'
        return result and result or False

    def act_finish(self):
        result = self.state = 'finish'
        return result and result or False

    def act_cancel(self):
        self.state = 'cancel'

    def act_set_to_draft(self):
        self.state = 'draft'
