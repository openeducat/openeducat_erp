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

MATCH_STATUS = [
    ('not_evaluated', 'Not Evaluated'),
    ('eligible', 'Eligible'),
    ('conditionally_eligible', 'Conditionally Eligible'),
    ('not_eligible', 'Not Eligible'),
]


class OpCareerMatch(models.Model):
    """Links a student's predicted national-exam performance to a KUCCPS
    career/programme and indicates whether the student is likely to meet
    the entry requirements."""

    _name = 'op.career.match'
    _description = 'Student Career Suitability Match'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'student_id, match_status, career_id'

    student_id = fields.Many2one(
        'op.student', string='Student', required=True,
        ondelete='cascade', tracking=True, index=True)
    career_id = fields.Many2one(
        'op.kuccps.career', string='Career / Programme',
        required=True, ondelete='cascade', tracking=True)
    prediction_id = fields.Many2one(
        'op.national.exam.prediction',
        string='Based on Prediction',
        ondelete='set null')
    predicted_percentage = fields.Float(
        'Predicted Score (%)',
        related='prediction_id.predicted_percentage',
        store=True)
    minimum_points = fields.Float(
        'Required Points',
        related='career_id.minimum_points',
        store=True)
    match_status = fields.Selection(
        MATCH_STATUS, string='Suitability',
        default='not_evaluated', tracking=True)
    match_score = fields.Float(
        'Match Score (%)', digits=(5, 2),
        help="How well the student's profile matches career requirements")
    evaluation_date = fields.Datetime('Evaluated On')
    counsellor_notes = fields.Text('Counsellor Notes')

    _sql_constraints = [
        ('unique_student_career',
         'unique(student_id, career_id)',
         'A career match record already exists for this student and career!'),
    ]

    def action_evaluate_match(self):
        """Simple heuristic match: compare predicted percentage against the
        career minimum points (treated as a percentage for CBC data).
        Upgrade to a full subject-combination check as data matures."""
        for rec in self:
            predicted = rec.predicted_percentage
            required = rec.career_id.minimum_points
            if required <= 0:
                rec.match_status = 'not_evaluated'
                rec.match_score = 0.0
            elif predicted >= required:
                rec.match_status = 'eligible'
                rec.match_score = min(
                    100.0, (predicted / required) * 100.0)
            elif predicted >= required * 0.85:
                rec.match_status = 'conditionally_eligible'
                rec.match_score = (predicted / required) * 100.0
            else:
                rec.match_status = 'not_eligible'
                rec.match_score = (predicted / required) * 100.0
            rec.evaluation_date = fields.Datetime.now()
        return True

    @api.model
    def generate_matches_for_student(self, student_id):
        """Auto-generate career match records for every active KUCCPS career
        using the student's Grade 12 prediction (or the latest available)."""
        student = self.env['op.student'].browse(student_id)
        prediction = self.env['op.national.exam.prediction'].search([
            ('student_id', '=', student.id),
            ('national_exam_grade', '=', 'grade_12'),
            ('state', 'in', ['computed', 'confirmed']),
        ], order='computation_date desc', limit=1)
        if not prediction:
            prediction = self.env['op.national.exam.prediction'].search([
                ('student_id', '=', student.id),
                ('state', 'in', ['computed', 'confirmed']),
            ], order='computation_date desc', limit=1)
        careers = self.env['op.kuccps.career'].search([
            ('active', '=', True)])
        created = 0
        for career in careers:
            existing = self.search([
                ('student_id', '=', student.id),
                ('career_id', '=', career.id),
            ], limit=1)
            if not existing:
                self.create({
                    'student_id': student.id,
                    'career_id': career.id,
                    'prediction_id': prediction.id if prediction else False,
                })
                created += 1
        self.search([
            ('student_id', '=', student.id),
            ('match_status', '=', 'not_evaluated'),
        ]).action_evaluate_match()
        return created
