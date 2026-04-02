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

from .test_fees_common import TestFeesCommon
from odoo.exceptions import AccessError, UserError
from odoo import fields


class TestStudentFees(TestFeesCommon):
    """Tests for op.student.fees.details model"""

    def setUp(self):
        super(TestStudentFees, self).setUp()

    def test_01_fees_record_creation(self):
        """Test creating a student fees record directly"""
        student = self.env.ref('openeducat_core.op_student_1')
        fee = self.op_student_fees.create({
            'student_id': student.id,
            'amount': 5000.0,
            'state': 'draft',
            'date': fields.Date.today(),
        })
        self.assertTrue(fee.id)
        self.assertEqual(fee.student_id, student)
        self.assertEqual(fee.state, 'draft')
        self.assertEqual(fee.amount, 5000.0)

    def test_02_fees_discount_computation(self):
        """Test that after_discount_amount is correctly computed"""
        student = self.env.ref('openeducat_core.op_student_1')
        fee = self.op_student_fees.create({
            'student_id': student.id,
            'amount': 10000.0,
            'discount': 10.0,
            'state': 'draft',
        })
        fee._compute_discount_amount()
        # 10% off 10000 = 9000
        self.assertAlmostEqual(fee.after_discount_amount, 9000.0)

    def test_03_fees_action_get_invoice_no_invoice(self):
        """Test action_get_invoice returns True when no invoice exists"""
        student = self.env.ref('openeducat_core.op_student_1')
        fee = self.op_student_fees.create({
            'student_id': student.id,
            'amount': 500.0,
            'state': 'draft',
        })
        result = fee.action_get_invoice()
        self.assertTrue(result)

    def test_04_fees_action_get_invoice_with_invoice(self):
        """Test action_get_invoice opens invoice form when invoice exists"""
        student = self.env.ref('openeducat_core.op_student_1')
        fee = self.op_student_fees.create({
            'student_id': student.id,
            'amount': 500.0,
            'state': 'draft',
        })
        # Manually attach a dummy invoice
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': student.partner_id.id,
        })
        fee.invoice_id = invoice.id
        result = fee.action_get_invoice()
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get('res_id'), invoice.id)

    def test_05_student_fees_count_compute(self):
        """Test fees_details_count is computed from linked fee records"""
        student = self.env.ref('openeducat_core.op_student_1')
        initial_count = student.fees_details_count

        self.op_student_fees.create({'student_id': student.id, 'amount': 100.0})
        self.op_student_fees.create({'student_id': student.id, 'amount': 200.0})

        student._compute_fees_details()
        self.assertEqual(student.fees_details_count, initial_count + 2)


class TestFeesTerms(TestFeesCommon):
    """Tests for op.fees.terms model"""

    def setUp(self):
        super(TestFeesTerms, self).setUp()

    def test_01_fees_terms_valid_creation(self):
        """Test creating a valid fees term with lines summing to 100%"""
        term = self.op_fees_terms.create({
            'name': 'Annual Fixed Term',
            'code': 'AFT001',
            'fees_terms': 'fixed_days',
            'line_ids': [(0, 0, {
                'due_days': 30,
                'value': 100.0,
            })]
        })
        self.assertTrue(term.id)
        self.assertEqual(len(term.line_ids), 1)
        self.assertEqual(term.line_ids[0].value, 100.0)

    def test_02_fees_terms_invalid_no_lines(self):
        """Test that removing all lines from a term raises AccessError"""
        # First create a valid term with a line
        term = self.op_fees_terms.create({
            'name': 'No Lines Term',
            'code': 'NLT001',
            'line_ids': [(0, 0, {'due_days': 30, 'value': 100.0})]
        })
        # Now remove all lines via write to trigger the constraint
        with self.assertRaises(AccessError):
            term.write({'line_ids': [(5, 0, 0)]})

    def test_03_fees_terms_invalid_percent_sum(self):
        """Test that lines not summing to 100 raises AccessError"""
        with self.assertRaises(AccessError):
            self.op_fees_terms.create({
                'name': 'Bad Percent Term',
                'code': 'BPT001',
                'line_ids': [(0, 0, {
                    'due_days': 30,
                    'value': 60.0,
                })]
            })

    def test_04_fees_terms_multi_installments(self):
        """Test a term with multiple installment lines summing to 100%"""
        term = self.op_fees_terms.create({
            'name': 'Semester Term',
            'code': 'SMT002',
            'fees_terms': 'fixed_date',
            'line_ids': [
                (0, 0, {'due_days': 10, 'value': 50.0}),
                (0, 0, {'due_days': 60, 'value': 50.0}),
            ]
        })
        self.assertTrue(term.id)
        self.assertEqual(len(term.line_ids), 2)

    def test_05_fees_terms_discount(self):
        """Test discount field is saved on fees terms"""
        term = self.op_fees_terms.create({
            'name': 'Discount Term',
            'code': 'DT003',
            'discount': 15.0,
            'line_ids': [(0, 0, {'due_days': 30, 'value': 100.0})]
        })
        self.assertEqual(term.discount, 15.0)


class TestWizardFees(TestFeesCommon):
    """Tests for fees.detail.report.wizard model"""

    def setUp(self):
        super(TestWizardFees, self).setUp()

    def test_01_wizard_filter_by_student(self):
        """Test the fees report wizard filtered by student"""
        wizard = self.op_fees_wizard.create({
            'fees_filter': 'student',
            'student_id': self.env.ref('openeducat_core.op_student_1').id
        })
        self.assertTrue(wizard.id)
        self.assertEqual(wizard.fees_filter, 'student')
        wizard.print_report()

    def test_02_wizard_filter_by_course(self):
        """Test the fees report wizard filtered by course"""
        wizard = self.op_fees_wizard.create({
            'fees_filter': 'course',
            'course_id': self.env.ref('openeducat_core.op_course_1').id,
        })
        self.assertTrue(wizard.id)
        wizard.print_report()

    def test_03_wizard_filter_by_student_report(self):
        """Test that print_report returns a report action for student filter"""
        student = self.env.ref('openeducat_core.op_student_2')
        wizard = self.op_fees_wizard.create({
            'fees_filter': 'student',
            'student_id': student.id,
        })
        result = wizard.print_report()
        self.assertIsInstance(result, dict)
        self.assertIn('type', result)
