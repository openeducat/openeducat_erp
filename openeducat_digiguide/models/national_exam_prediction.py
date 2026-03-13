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

# National exam grades in Kenya's CBC curriculum
NATIONAL_EXAM_GRADES = [
    ('grade_3', 'Grade 3 (Primary)'),
    ('grade_6', 'Grade 6 (Upper Primary)'),
    ('grade_9', 'Grade 9 (Junior Secondary)'),
    ('grade_12', 'Grade 12 (Senior Secondary)'),
]

PREDICTION_STATUS = [
    ('draft', 'Draft'),
    ('computed', 'Computed'),
    ('confirmed', 'Confirmed'),
]


class OpNationalExamPrediction(models.Model):
    """Holds a predicted national-exam performance score for a student
    computed from their historical CBC academic performance data.

    * Grade 3  – predicted from Grades 1, 2 and 3 continuous assessment
    * Grade 6  – predicted from Grades 1-6 continuous assessment
    * Grade 9  – predicted from Grades 7, 8 and 9 continuous assessment
    * Grade 12 – predicted from Grades 10, 11 and 12 continuous assessment
    """

    _name = 'op.national.exam.prediction'
    _description = 'National Exam Performance Prediction'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'student_id, national_exam_grade'

    student_id = fields.Many2one(
        'op.student', string='Student', required=True,
        ondelete='cascade', tracking=True, index=True)
    national_exam_grade = fields.Selection(
        NATIONAL_EXAM_GRADES, string='National Exam', required=True,
        tracking=True)
    predicted_percentage = fields.Float(
        'Predicted Score (%)', digits=(5, 2), tracking=True)
    predicted_grade_letter = fields.Char(
        'Predicted Grade', compute='_compute_predicted_letter',
        store=True)
    confidence_level = fields.Float(
        'Confidence (%)', digits=(5, 2),
        help="Statistical confidence in the prediction (0–100 %)")
    computation_date = fields.Datetime(
        'Computed On', default=fields.Datetime.now)
    state = fields.Selection(
        PREDICTION_STATUS, string='Status', default='draft',
        tracking=True)
    performance_ids = fields.Many2many(
        'op.academic.performance',
        'op_prediction_performance_rel',
        'prediction_id', 'performance_id',
        string='Source Performance Records')
    notes = fields.Text('Analyst Notes')

    _sql_constraints = [
        ('unique_student_exam',
         'unique(student_id, national_exam_grade)',
         'A prediction already exists for this student and national exam!'),
    ]

    @api.depends('predicted_percentage')
    def _compute_predicted_letter(self):
        for rec in self:
            p = rec.predicted_percentage
            if p >= 80:
                rec.predicted_grade_letter = 'A'
            elif p >= 70:
                rec.predicted_grade_letter = 'B'
            elif p >= 60:
                rec.predicted_grade_letter = 'C'
            elif p >= 50:
                rec.predicted_grade_letter = 'D'
            else:
                rec.predicted_grade_letter = 'E'

    def action_compute_prediction(self):
        """Compute a weighted-average prediction from the student's historical
        performance records for the grades that feed into this national exam.

        Grade 3  ← grades 1, 2, 3
        Grade 6  ← grades 1, 2, 3, 4, 5, 6
        Grade 9  ← grades 7, 8, 9
        Grade 12 ← grades 10, 11, 12
        """
        grade_map = {
            'grade_3': ['grade_1', 'grade_2', 'grade_3'],
            'grade_6': [
                'grade_1', 'grade_2', 'grade_3',
                'grade_4', 'grade_5', 'grade_6',
            ],
            'grade_9': ['grade_7', 'grade_8', 'grade_9'],
            'grade_12': ['grade_10', 'grade_11', 'grade_12'],
        }
        for rec in self:
            source_grades = grade_map.get(rec.national_exam_grade, [])
            performances = self.env['op.academic.performance'].search([
                ('student_id', '=', rec.student_id.id),
                ('grade', 'in', source_grades),
            ])
            if performances:
                avg = sum(performances.mapped('percentage')) / len(performances)
                rec.predicted_percentage = round(avg, 2)
                rec.performance_ids = [(6, 0, performances.ids)]
                # Confidence increases with more data points (capped at 95 %)
                count = len(performances)
                rec.confidence_level = min(95.0, 50.0 + count * 2.0)
            else:
                rec.predicted_percentage = 0.0
                rec.confidence_level = 0.0
            rec.computation_date = fields.Datetime.now()
            rec.state = 'computed'
        return True

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_reset_draft(self):
        self.write({'state': 'draft'})
