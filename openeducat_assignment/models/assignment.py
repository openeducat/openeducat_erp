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

from odoo import _, api, fields, models
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
    ], 'Status', required=True, default='draft', tracking=True)
    submission_date = fields.Datetime('Submission Date', required=True,
                                      tracking=True)
    allocation_ids = fields.Many2many('op.student', string='Allocated To')
    assignment_sub_line = fields.One2many('op.assignment.sub.line',
                                          'assignment_id', 'Submission')
    reviewer = fields.Many2one('op.faculty', 'Reviewer')
    active = fields.Boolean(default=True)
    grading_assignment_id = fields.Many2one('grading.assignment', 'Grading Assignment',
                                            required=True, ondelete="cascade")
    assignment_sub_line_count = fields.Integer(
        'Submissions', compute="_compute_assignment_count_compute")
    courses_subjects = fields.Many2many('op.subject')

    @api.constrains('issued_date', 'submission_date')
    def check_dates(self):
        for record in self:
            issued_date = fields.Date.from_string(record.issued_date)
            submission_date = fields.Date.from_string(record.submission_date)
            if issued_date > submission_date:
                raise ValidationError(_(
                    "Submission Date cannot be set before Issue Date."))

    @api.constrains('marks')
    def _check_marks(self):
        for record in self:
            if record.marks < 0:
                raise ValidationError(_("Marks cannot be negative!"))

    def _compute_assignment_count_compute(self):
        self.assignment_sub_line_count = len(self.assignment_sub_line)

    @api.onchange('course_id')
    def onchange_course(self):
        # Course change resets both the batch and the allocation. The
        # cleared batch triggers `onchange_batch_id` on the next tick
        # (with a False batch → allocation stays empty), so the two
        # side-effects compose safely.
        self.batch_id = False
        self.allocation_ids = [(5, 0, 0)]
        if self.course_id:
            subject_ids = self.env['op.course'].search([
                ('id', '=', self.course_id.id)]).subject_ids
            return {'domain': {'subject_id': [('id', 'in', subject_ids.ids)]}}

    @api.onchange('course_id')
    def onchange_subjects(self):
        for rec in self:
            if rec.course_id:
                rec.courses_subjects = rec.course_id.subject_ids

    @api.onchange('batch_id')
    def onchange_batch_id_populate_allocation(self):
        """Auto-populate `allocation_ids` with every student enrolled
        in the chosen batch. Users can still prune the list manually —
        the assignment editor sees the full roster pre-populated and
        can drop individuals if the work isn't for everyone.

        Reads through `op.student.course` (the enrollment link
        table) rather than `op.student` directly, so students who
        transferred courses or are inactive in this batch don't leak
        in from other batches they've been in.
        """
        if not self.batch_id:
            self.allocation_ids = [(5, 0, 0)]
            return
        enrollments = self.env['op.student.course'].search(
            [('batch_id', '=', self.batch_id.id)]
        )
        self.allocation_ids = [(6, 0, enrollments.mapped('student_id').ids)]

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

    def get_assignment_submissions(self):
        return {
            'name': 'Assignment Submissions',
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'op.assignment.sub.line',
            'domain': [('id', 'in', self.assignment_sub_line.ids)],
            'target': 'current',
        }
