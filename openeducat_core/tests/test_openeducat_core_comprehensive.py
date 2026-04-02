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

from .test_core_common import TestCoreCommon
from odoo.tests import Form
from odoo.exceptions import ValidationError, AccessError
from odoo import fields
from datetime import timedelta, date


class TestOpenEduCatCoreComprehensive(TestCoreCommon):

    def setUp(self):
        super(TestOpenEduCatCoreComprehensive, self).setUp()
        self.Student = self.env['op.student']
        self.Faculty = self.env['op.faculty']
        self.Course = self.env['op.course']
        self.Batch = self.env['op.batch']
        self.Subject = self.env['op.subject']
        self.SubjectRegistration = self.env['op.subject.registration']
        self.AcademicYear = self.env['op.academic.year']
        self.AcademicTerm = self.env['op.academic.term']
        self.Category = self.env['op.category']

        # Setup standard data for tests
        self.course_1 = self.Course.create({
            'name': 'B.Sc. IT',
            'code': 'BSCIT',
        })
        self.batch_1 = self.Batch.create({
            'name': '2025-27',
            'code': 'B2527',
            'course_id': self.course_1.id,
            'start_date': fields.Date.today(),
            'end_date': fields.Date.today() + timedelta(days=365),
        })
        self.subject_1 = self.Subject.create({
            'name': 'Python Programming',
            'code': 'PY001',
            'subject_type': 'compulsory',
        })
        self.course_1.subject_ids = [(4, self.subject_1.id)]

    def test_01_student_full_lifecycle(self):
        """Test Student Lifecycle: Create, Read, Update, Delete"""
        with Form(self.Student) as f:
            f.first_name = 'Harry'
            f.last_name = 'Potter'
            f.birth_date = '2000-07-31'
            f.gender = 'm'
            f.email = 'harry@hogwarts.edu'
            f.gr_no = 'GR007'
            student = f.save()
            
        self.assertTrue(student.id)
        self.assertEqual(student.name, "Harry Potter")

        # Update
        student.write({'name': 'Harry James Potter', 'middle_name': 'James'})
        self.assertEqual(student.name, "Harry James Potter")

        # Business Methods
        student.create_student_user()
        self.assertTrue(student.user_id)

    def test_02_faculty_full_lifecycle(self):
        """Test Faculty Lifecycle"""
        with Form(self.Faculty) as f:
            f.first_name = 'Severus'
            f.last_name = 'Snape'
            f.birth_date = '1960-01-09'
            f.gender = 'male'
            f.email = 'snape@hogwarts.edu'
            faculty = f.save()

        self.assertTrue(faculty.id)
        self.assertEqual(faculty.name, "Severus Snape")

        # Business Method: Create Employee
        faculty.create_employee()
        self.assertTrue(faculty.emp_id)

    def test_03_business_rules_validation(self):
        """Test validations"""
        with self.assertRaises(ValidationError):
            with Form(self.Student) as f:
                f.first_name = 'Future'
                f.last_name = 'Born'
                f.birth_date = fields.Date.today() + timedelta(days=5)
                f.gender = 'm'
                f.save()

        # Test Category Assignment
        cat = self.Category.create({'name': 'General','code':'gen_1'})
        with Form(self.Student) as f:
            f.first_name = 'Cat'
            f.last_name = 'Test'
            f.gender = 'm'
            f.category_id = cat
            student = f.save()
        self.assertEqual(student.category_id, cat)

    def test_04_academic_structure_logic(self):
        """Test Academic Year and Term creation logic"""
        ay = self.AcademicYear.create({
            'name': 'AY 2025 Test',
            'start_date': fields.Date.today(),
            'end_date': fields.Date.today() + timedelta(days=365),
            'term_structure': 'three_sem',
        })
        ay.term_create()
        self.assertEqual(len(ay.academic_term_ids), 3)
        
    def test_05_subject_registration_process(self):
        """Test the registration workflow"""
        with Form(self.Student) as f:
            f.first_name = 'Bob'
            f.last_name = 'Builder'
            f.gender = 'm'
            student = f.save()
            
        self.env['op.student.course'].create({
            'student_id': student.id,
            'course_id': self.course_1.id,
            'batch_id': self.batch_1.id,
        })

        reg = self.SubjectRegistration.create({
            'student_id': student.id,
            'course_id': self.course_1.id,
            'batch_id': self.batch_1.id,
        })
        reg.get_subjects()
        reg.action_submitted()
        reg.action_approve()
        self.assertEqual(reg.state, 'approved')

    def test_06_security_record_rules(self):
        """Test data isolation via record rules"""
        faculty_user = self.env['res.users'].create({
            'name': 'Faculty User',
            'login': 'faculty_u',
            'email': 'faculty_u@test.com',
            'group_ids': [(6, 0, [self.env.ref('openeducat_core.group_op_faculty').id])]
        })
        
        fac_self = self.Faculty.create({
            'name': 'Self Prof',
            'first_name': 'Self', 'last_name': 'Prof', 'birth_date': '1990-01-01',
            'gender': 'male', 'user_id': faculty_user.id
        })
        fac_other = self.Faculty.create({
            'name': 'Other Prof',
            'first_name': 'Other', 'last_name': 'Prof', 'birth_date': '1990-01-01',
            'gender': 'female'
        })
        
        faculty_env = self.env(user=faculty_user)
        visible_facs = faculty_env['op.faculty'].search([])
        self.assertIn(fac_self.id, visible_facs.ids)
        self.assertNotIn(fac_other.id, visible_facs.ids)

    def test_07_view_integration(self):
        """Ensure form views load correctly and maintain defaults"""
        with Form(self.Student) as student_form:
            student_form.first_name = 'Integrated'
            student_form.last_name = 'Test'
            student_form.gender = 'f'
            student_form.birth_date = '2005-01-01'
            s_rec = student_form.save()
            self.assertTrue(s_rec.id)
            
        # Batch Form View Check
        with Form(self.Batch) as batch_form:
            batch_form.name = 'Test Form Batch'
            batch_form.code = 'FTB'
            batch_form.course_id = self.course_1
            batch_form.start_date = fields.Date.today()
            batch_form.end_date = fields.Date.today() + timedelta(days=365)
            b_rec = batch_form.save()
            self.assertEqual(b_rec.course_id, self.course_1)

    def test_08_helper_methods_and_crons(self):
        """Test misc methods and crons"""
        reg = self.SubjectRegistration.create({
            'course_id': self.course_1.id,
        })
        self.assertNotEqual(reg.name, 'New')
