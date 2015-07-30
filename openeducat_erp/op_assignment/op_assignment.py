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

from openerp import models, fields, api


class OpAssignment(models.Model):
    _name = 'op.assignment'

    name = fields.Char('Name', size=16, required=True)
    course_id = fields.Many2one('op.course', 'Course', required=True)
    standard_id = fields.Many2one('op.standard', 'Standard', required=True)
    division_id = fields.Many2one('op.division', 'Division')
    subject_id = fields.Many2one('op.subject', 'Subject', required=True)
    faculty_id = fields.Many2one('op.faculty', 'Faculty', required=True)
    marks = fields.Float('Marks')
    description = fields.Text('Description', required=True)
    type = fields.Many2one('op.exam.type', 'Type', required=True)
    state = fields.Selection(
        [('d', 'Draft'), ('p', 'Publish'), ('f', 'Finished')], 'State',
        required=True, default='d')
    issued_date = fields.Datetime('Issued Date', required=True)
    submission_date = fields.Datetime('Submission Date', required=True)
    allocation_ids = fields.Many2many('op.student', string='Allocated To')
    assignment_sub_line = fields.One2many(
        'op.assignment.sub.line', 'assignment_id', 'Submissions')
    reviewer = fields.Many2one('op.faculty', 'Reviewer')

    @api.one
    def act_draft(self):
        # Reminder:: Delete this method as it is not used.
        self.state = 'd'

    @api.one
    def act_publish(self):
        self.state = 'p'

    @api.one
    def act_finish(self):
        self.state = 'f'


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
