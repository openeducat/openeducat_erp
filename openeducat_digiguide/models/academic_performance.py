###############################################################################
#
#    openEMIS
#    Copyright (C) 2009-TODAY openEMIS(<https://www.openemis.org>).
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


CBC_GRADES = [
    ('grade_1', 'Grade 1'),
    ('grade_2', 'Grade 2'),
    ('grade_3', 'Grade 3'),
    ('grade_4', 'Grade 4'),
    ('grade_5', 'Grade 5'),
    ('grade_6', 'Grade 6'),
    ('grade_7', 'Grade 7'),
    ('grade_8', 'Grade 8'),
    ('grade_9', 'Grade 9'),
    ('grade_10', 'Grade 10'),
    ('grade_11', 'Grade 11'),
    ('grade_12', 'Grade 12'),
]

ASSESSMENT_TYPES = [
    ('weekly_assignment', 'Weekly Assignment'),
    ('mid_term', 'Mid Term Exam'),
    ('termly', 'Termly Exam'),
    ('annual', 'Annual / End of Year Exam'),
]

TERM_CHOICES = [
    ('term_1', 'Term 1'),
    ('term_2', 'Term 2'),
    ('term_3', 'Term 3'),
]


class OpAcademicPerformance(models.Model):
    """Records a single assessment score for a student in a specific subject,
    grade, term and academic year.  These records are the raw input used by the
    national-exam prediction engine."""

    _name = 'op.academic.performance'
    _description = 'Student Academic Performance Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'academic_year desc, grade desc, term, assessment_type'

    student_id = fields.Many2one(
        'op.student', string='Student', required=True,
        ondelete='cascade', tracking=True,
        index=True)
    subject_id = fields.Many2one(
        'op.subject', string='Subject', required=True,
        ondelete='restrict', tracking=True)
    academic_year = fields.Char(
        'Academic Year', required=True, tracking=True,
        help="e.g. 2024")
    grade = fields.Selection(
        CBC_GRADES, string='Grade Level', required=True, tracking=True)
    term = fields.Selection(
        TERM_CHOICES, string='Term', required=True, tracking=True)
    assessment_type = fields.Selection(
        ASSESSMENT_TYPES, string='Assessment Type', required=True,
        tracking=True)
    score = fields.Float(
        'Score (%)', required=True,
        help="Score as a percentage (0 – 100)")
    max_score = fields.Float(
        'Maximum Score', default=100.0,
        help="Total marks available for this assessment")
    percentage = fields.Float(
        'Percentage', compute='_compute_percentage',
        store=True, digits=(5, 2))
    grade_letter = fields.Char(
        'Grade Letter', compute='_compute_grade_letter', store=True)
    notes = fields.Text('Notes / Remarks')
    is_national_exam_grade = fields.Boolean(
        'National Exam Grade?',
        default=False,
        help="Tick if this score is from a national examination "
             "(Grade 3, 6, 9 or 12)")

    @api.depends('score', 'max_score')
    def _compute_percentage(self):
        for rec in self:
            if rec.max_score and rec.max_score > 0:
                rec.percentage = (rec.score / rec.max_score) * 100.0
            else:
                rec.percentage = 0.0

    @api.depends('percentage')
    def _compute_grade_letter(self):
        for rec in self:
            p = rec.percentage
            if p >= 80:
                rec.grade_letter = 'A'
            elif p >= 70:
                rec.grade_letter = 'B'
            elif p >= 60:
                rec.grade_letter = 'C'
            elif p >= 50:
                rec.grade_letter = 'D'
            else:
                rec.grade_letter = 'E'

    @api.constrains('score', 'max_score')
    def _check_score(self):
        for rec in self:
            if rec.score < 0:
                raise ValidationError(_("Score cannot be negative."))
            if rec.max_score <= 0:
                raise ValidationError(
                    _("Maximum score must be greater than zero."))
            if rec.score > rec.max_score:
                raise ValidationError(
                    _("Score (%s) cannot exceed maximum score (%s).")
                    % (rec.score, rec.max_score))
