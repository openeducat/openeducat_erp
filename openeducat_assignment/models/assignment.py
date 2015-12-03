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


class OpAssignment(models.Model):
    _name = 'op.assignment'
    _inherit = 'mail.thread'
    _description = 'Assignment'

    name = fields.Char('Name', size=16, required=True)
    course_id = fields.Many2one('op.course', 'Course', required=True)
    batch_id = fields.Many2one('op.batch', 'Batch', required=True)
    subject_id = fields.Many2one('op.subject', 'Subject', required=True)
    faculty_id = fields.Many2one(
        'op.faculty', 'Faculty', default=lambda self: self.env[
            'op.faculty'].search([('user_id', '=', self.env.uid)]),
        required=True)
    assignment_type_id = fields.Many2one(
        'op.assignment.type', 'Assignment Type', required=True)
    marks = fields.Float('Marks', track_visibility='onchange')
    description = fields.Text('Description', required=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('publish', 'Published'),
         ('finish', 'Finished')], 'State', required=True, default='draft',
        track_visibility='onchange')
    issued_date = fields.Datetime(
        'Issued Date', required=True,
        default=lambda self: fields.Datetime.now())
    submission_date = fields.Datetime(
        'Submission Date', required=True,
        track_visibility='onchange')
    allocation_ids = fields.Many2many('op.student', string='Allocated To')
    assignment_sub_line = fields.One2many(
        'op.assignment.sub.line', 'assignment_id', 'Submissions')
    reviewer = fields.Many2one('op.faculty', 'Reviewer')

    @api.one
    @api.constrains('issued_date', 'submission_date')
    def check_dates(self):
        issued_date = fields.Date.from_string(self.issued_date)
        submission_date = fields.Date.from_string(self.submission_date)
        if issued_date > submission_date:
            raise ValidationError(
                "Submission Date cannot be set before Issue Date.")

    @api.onchange('course_id')
    def onchange_course(self):
        self.batch_id = False

    @api.one
    def act_publish(self):
        self.state = 'publish'

    @api.one
    def act_finish(self):
        self.state = 'finish'


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
