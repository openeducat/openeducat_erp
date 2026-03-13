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

from odoo.tests.common import TransactionCase


class TestDigiGuide(TransactionCase):
    """Basic unit tests for the DigiGuide module."""

    def setUp(self):
        super(TestDigiGuide, self).setUp()
        # Create a minimal student for testing
        partner = self.env['res.partner'].create({'name': 'Test Student DG'})
        self.student = self.env['op.student'].create({
            'first_name': 'Test',
            'last_name': 'Student',
            'gender': 'm',
            'partner_id': partner.id,
            'gr_no': 'TST-DG-001',
        })
        self.subject = self.env['op.subject'].create({
            'name': 'Mathematics',
            'code': 'MATH-DG',
        })

    def test_academic_performance_percentage(self):
        perf = self.env['op.academic.performance'].create({
            'student_id': self.student.id,
            'subject_id': self.subject.id,
            'academic_year': '2024',
            'grade': 'grade_3',
            'term': 'term_1',
            'assessment_type': 'mid_term',
            'score': 75.0,
            'max_score': 100.0,
        })
        self.assertAlmostEqual(perf.percentage, 75.0)
        self.assertEqual(perf.grade_letter, 'B')

    def test_academic_performance_grade_letter(self):
        cases = [
            (85, 'A'), (75, 'B'), (65, 'C'), (55, 'D'), (40, 'E')
        ]
        for score, expected_letter in cases:
            perf = self.env['op.academic.performance'].create({
                'student_id': self.student.id,
                'subject_id': self.subject.id,
                'academic_year': '2024',
                'grade': 'grade_1',
                'term': 'term_2',
                'assessment_type': 'weekly_assignment',
                'score': score,
                'max_score': 100.0,
            })
            self.assertEqual(
                perf.grade_letter, expected_letter,
                "Expected %s for score %s" % (expected_letter, score))

    def test_national_exam_prediction_compute(self):
        # Create performance records
        for grade in ['grade_1', 'grade_2', 'grade_3']:
            self.env['op.academic.performance'].create({
                'student_id': self.student.id,
                'subject_id': self.subject.id,
                'academic_year': '2024',
                'grade': grade,
                'term': 'term_1',
                'assessment_type': 'termly',
                'score': 70.0,
                'max_score': 100.0,
            })
        prediction = self.env['op.national.exam.prediction'].create({
            'student_id': self.student.id,
            'national_exam_grade': 'grade_3',
        })
        prediction.action_compute_prediction()
        self.assertEqual(prediction.state, 'computed')
        self.assertAlmostEqual(prediction.predicted_percentage, 70.0)
        self.assertEqual(prediction.predicted_grade_letter, 'B')

    def test_career_match_eligible(self):
        prediction = self.env['op.national.exam.prediction'].create({
            'student_id': self.student.id,
            'national_exam_grade': 'grade_12',
            'predicted_percentage': 75.0,
            'state': 'computed',
        })
        career = self.env['op.kuccps.career'].create({
            'name': 'Test Career',
            'kuccps_code': 'TST001',
            'minimum_points': 60.0,
        })
        match = self.env['op.career.match'].create({
            'student_id': self.student.id,
            'career_id': career.id,
            'prediction_id': prediction.id,
        })
        match.action_evaluate_match()
        self.assertEqual(match.match_status, 'eligible')

    def test_career_match_not_eligible(self):
        prediction = self.env['op.national.exam.prediction'].create({
            'student_id': self.student.id,
            'national_exam_grade': 'grade_12',
            'predicted_percentage': 40.0,
            'state': 'computed',
        })
        career = self.env['op.kuccps.career'].create({
            'name': 'Test Career 2',
            'kuccps_code': 'TST002',
            'minimum_points': 70.0,
        })
        match = self.env['op.career.match'].create({
            'student_id': self.student.id,
            'career_id': career.id,
            'prediction_id': prediction.id,
        })
        match.action_evaluate_match()
        self.assertEqual(match.match_status, 'not_eligible')
