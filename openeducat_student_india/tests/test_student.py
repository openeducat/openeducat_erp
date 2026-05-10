from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestOpStudentIndia(TransactionCase):
    """Test cases for India-specific student customization"""

    def setUp(self):
        super().setUp()
        # Create a test partner (student requires a partner)
        self.partner = self.env['res.partner'].create({
            'name': 'Test Student Partner',
            'email': 'test.student@example.com',
        })

    def test_aadhar_valid_format(self):
        """Test that valid Aadhar numbers are accepted"""
        student = self.env['op.student'].create({
            'first_name': 'Rajesh',
            'last_name': 'Kumar',
            'gender': 'm',
            'partner_id': self.partner.id,
            'aadhar_number': '123456789012',
            'religion': 'hindu',
            'caste': 'general',
        })
        self.assertEqual(student.aadhar_number, '123456789012')
        self.assertEqual(student.religion, 'hindu')
        self.assertEqual(student.caste, 'general')

    def test_aadhar_invalid_format_too_short(self):
        """Test that Aadhar numbers with less than 12 digits are rejected"""
        with self.assertRaises(ValidationError) as context:
            self.env['op.student'].create({
                'first_name': 'Rajesh',
                'last_name': 'Kumar',
                'gender': 'm',
                'partner_id': self.partner.id,
                'aadhar_number': '12345678901',  # Only 11 digits
            })
        self.assertIn('12 digits', str(context.exception))

    def test_aadhar_invalid_format_too_long(self):
        """Test that Aadhar numbers with more than 12 digits are rejected"""
        with self.assertRaises(ValidationError) as context:
            self.env['op.student'].create({
                'first_name': 'Rajesh',
                'last_name': 'Kumar',
                'gender': 'm',
                'partner_id': self.partner.id,
                'aadhar_number': '1234567890123',  # 13 digits
            })
        self.assertIn('12 digits', str(context.exception))

    def test_aadhar_invalid_format_non_numeric(self):
        """Test that Aadhar numbers with non-numeric characters are rejected"""
        with self.assertRaises(ValidationError) as context:
            self.env['op.student'].create({
                'first_name': 'Rajesh',
                'last_name': 'Kumar',
                'gender': 'm',
                'partner_id': self.partner.id,
                'aadhar_number': '123456789ABC',  # Contains letters
            })
        self.assertIn('12 digits', str(context.exception))

    def test_aadhar_unique_constraint(self):
        """Test that duplicate Aadhar numbers are rejected"""
        # Create first student
        self.env['op.student'].create({
            'first_name': 'Rajesh',
            'last_name': 'Kumar',
            'gender': 'm',
            'partner_id': self.partner.id,
            'aadhar_number': '123456789012',
        })

        # Create second partner for second student
        partner2 = self.env['res.partner'].create({
            'name': 'Test Student 2',
            'email': 'test2@example.com',
        })

        # Try to create second student with same Aadhar
        with self.assertRaises(Exception) as context:  # IntegrityError wrapped
            self.env['op.student'].create({
                'first_name': 'Priya',
                'last_name': 'Singh',
                'gender': 'f',
                'partner_id': partner2.id,
                'aadhar_number': '123456789012',  # Duplicate
            })
        self.assertIn('unique', str(context.exception).lower())

    def test_aadhar_optional(self):
        """Test that Aadhar number is optional"""
        student = self.env['op.student'].create({
            'first_name': 'Priya',
            'last_name': 'Singh',
            'gender': 'f',
            'partner_id': self.partner.id,
            # No aadhar_number provided
        })
        self.assertEqual(student.aadhar_number, False)

    def test_religion_selection_options(self):
        """Test that religion field accepts valid options"""
        religions = ['hindu', 'muslim', 'christian', 'sikh', 'buddhist', 'jain', 'other']
        for religion in religions:
            student = self.env['op.student'].create({
                'first_name': f'Student_{religion}',
                'last_name': 'Test',
                'gender': 'm',
                'partner_id': self.partner.id,
                'religion': religion,
            })
            self.assertEqual(student.religion, religion)

    def test_caste_selection_options(self):
        """Test that caste field accepts valid options"""
        castes = ['general', 'sc', 'st', 'obc_ncl', 'obc_cl']
        for caste in castes:
            partner = self.env['res.partner'].create({
                'name': f'Partner_{caste}',
                'email': f'test_{caste}@example.com',
            })
            student = self.env['op.student'].create({
                'first_name': f'Student_{caste}',
                'last_name': 'Test',
                'gender': 'm',
                'partner_id': partner.id,
                'caste': caste,
            })
            self.assertEqual(student.caste, caste)

    def test_visa_field_still_exists_in_db(self):
        """Test that visa_info field still exists for backward compatibility"""
        # This test verifies that the field exists in the database
        # even though it's hidden from the UI
        self.assertTrue(hasattr(self.env['op.student'], 'visa_info'))

    def test_nationality_field_still_exists_in_db(self):
        """Test that nationality field still exists for backward compatibility"""
        # This test verifies that the field exists in the database
        # even though it's hidden from the UI
        self.assertTrue(hasattr(self.env['op.student'], 'nationality'))
