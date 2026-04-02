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

from odoo.tests import TransactionCase
from odoo.exceptions import ValidationError, AccessError
from odoo import fields
import datetime


class TestAssignmentRobustCommon(TransactionCase):
    def setUp(self):
        super(TestAssignmentRobustCommon, self).setUp()
        self.Course = self.env['op.course']
        self.Batch = self.env['op.batch']
        self.Subject = self.env['op.subject']
        self.Faculty = self.env['op.faculty']
        self.Student = self.env['op.student']
        self.AssignmentType = self.env['grading.assignment.type']
        self.Assignment = self.env['op.assignment']
        self.Submission = self.env['op.assignment.sub.line']

        # Setup basic data
        self.course = self.Course.create({'name': 'Test Course', 'code': 'TC'})
        self.batch = self.Batch.create({
            'name': 'Test Batch', 
            'code': 'TB', 
            'course_id': self.course.id,
            'start_date': fields.Date.today(),
            'end_date': fields.Date.today() + datetime.timedelta(days=30)
        })
        self.subject = self.Subject.create({'name': 'Test Subject', 'code': 'TS'})
        
        self.faculty_user = self.env['res.users'].create({
            'name': 'Faculty User',
            'login': 'faculty_user_asg',
            'email': 'faculty_asg@test.com',
            'group_ids': [(6, 0, [self.env.ref('base.group_user').id])]
        })
        self.faculty = self.Faculty.create({
            'first_name': 'Faculty',
            'last_name': 'Test',
            'user_id': self.faculty_user.id,
            'gender': 'male',
            'birth_date': '1990-01-01'
        })
        
        self.student_user = self.env['res.users'].create({
            'name': 'Student User',
            'login': 'student_user_asg',
            'email': 'student_asg@test.com'
        })
        self.student = self.Student.create({
            'first_name': 'Student',
            'last_name': 'Test',
            'user_id': self.student_user.id,
            'gender': 'f',
            'birth_date': '2010-01-01'
        })
        
        self.asg_type = self.AssignmentType.create({
            'name': 'Homework',
            'code': 'HW',
            'assign_type': 'sub'
        })


class TestAssignmentModel(TestAssignmentRobustCommon):
    """Tests for op.assignment model"""

    def test_01_assignment_creation(self):
        """Test simple assignment creation and defaults"""
        asg = self.Assignment.create({
            'name': 'Assignment 01',
            'course_id': self.course.id,
            'batch_id': self.batch.id,
            'subject_id': self.subject.id,
            'faculty_id': self.faculty.id,
            'assignment_type': self.asg_type.id,
            'issued_date': fields.Datetime.now(),
            'submission_date': fields.Datetime.now() + datetime.timedelta(days=7),
            'marks': 100,
            'description': 'Test Assignment Description'
        })
        self.assertTrue(asg.id)
        self.assertEqual(asg.state, 'draft')
        self.assertEqual(asg.marks, 100)

    def test_02_assignment_date_constraint(self):
        """Test that submission_date cannot be before issued_date"""
        with self.assertRaises(ValidationError):
            self.Assignment.create({
                'name': 'Invalid Date Assignment',
                'course_id': self.course.id,
                'batch_id': self.batch.id,
                'assignment_type': self.asg_type.id,
                'faculty_id': self.faculty.id,
                'issued_date': fields.Datetime.now() + datetime.timedelta(days=1),
                'submission_date': fields.Datetime.now(),
                'description': 'Desc'
            })

    def test_03_assignment_state_transitions(self):
        """Test assignment state transitions (publish, finish, cancel, draft)"""
        asg = self.Assignment.create({
            'name': 'Transition Assignment',
            'course_id': self.course.id,
            'batch_id': self.batch.id,
            'assignment_type': self.asg_type.id,
            'faculty_id': self.faculty.id,
            'issued_date': fields.Datetime.now(),
            'submission_date': fields.Datetime.now() + datetime.timedelta(days=1),
            'description': 'Desc'
        })
        self.assertEqual(asg.state, 'draft')
        
        asg.act_publish()
        self.assertEqual(asg.state, 'publish')
        
        asg.act_finish()
        self.assertEqual(asg.state, 'finish')
        
        asg.act_cancel()
        self.assertEqual(asg.state, 'cancel')
        
        asg.act_set_to_draft()
        self.assertEqual(asg.state, 'draft')


class TestAssignmentSubmissionModel(TestAssignmentRobustCommon):
    """Tests for op.assignment.sub.line model"""

    def setUp(self):
        super(TestAssignmentSubmissionModel, self).setUp()
        self.asg = self.Assignment.create({
            'name': 'Parent Assignment',
            'course_id': self.course.id,
            'batch_id': self.batch.id,
            'assignment_type': self.asg_type.id,
            'faculty_id': self.faculty.id,
            'issued_date': fields.Datetime.now(),
            'submission_date': fields.Datetime.now() + datetime.timedelta(days=1),
            'marks': 100,
            'description': 'Desc'
        })

    def test_01_submission_creation(self):
        """Test student submission creation"""
        sub = self.Submission.create({
            'assignment_id': self.asg.id,
            'student_id': self.student.id,
            'description': 'My submission content'
        })
        self.assertTrue(sub.id)
        self.assertEqual(sub.state, 'draft')
        self.assertEqual(sub.submission_date.date(), fields.Date.today())

    def test_02_marks_validation(self):
        """Test that obtained marks cannot exceed total marks"""
        sub = self.Submission.create({
            'assignment_id': self.asg.id,
            'student_id': self.student.id,
        })
        # Assignment marks are 100
        with self.assertRaises(ValidationError):
            sub.write({'marks': 101})
        sub.write({'marks': 95}) # Should work

    def test_03_submission_unlink_constraint(self):
        """Test that none-draft submissions cannot be deleted by standard users"""
        sub = self.Submission.create({
            'assignment_id': self.asg.id,
            'student_id': self.student.id,
        })
        sub.act_submit()
        self.assertEqual(sub.state, 'submit')
        
        # Unlink should fail for submit state (unless in group_op_assignment_user)
        # We test as the superuser/test manager context here but let's check it doesn't raise if we didn't specify user
        # Actually in Odoo tests, by default you're UID 1 (Admin) who usually has all groups.
        # But the model code says "if not record.state == 'draft' and not self.env.user.has_group('openeducat_assignment.group_op_assignment_user')"
        # Administrator usually has that group.
        
        # Let's test negative deletion by a student user
        with self.assertRaises(ValidationError):
            sub.with_user(self.student_user).unlink()


class TestAssignmentTypeModel(TestAssignmentRobustCommon):
    """Tests for grading.assignment.type model"""

    def test_01_type_creation(self):
        """Test assignment type creation"""
        new_type = self.AssignmentType.create({
            'name': 'Project',
            'code': 'PRJ01',
            'assign_type': 'sub'
        })
        self.assertTrue(new_type.id)
        self.assertEqual(new_type.name, 'Project')

    def test_02_unique_code_constraint(self):
        """Test that code must be unique"""
        from odoo.tools import mute_logger
        from psycopg2 import IntegrityError
        
        self.AssignmentType.create({
            'name': 'Type 1',
            'code': 'UNIQUE_T001'
        })
        
        # We use a savepoint to allow recovery after a PostgreSQL error
        # and mute_logger to keep the logs clean
        with self.cr.savepoint(), mute_logger('odoo.sql_db'):
            with self.assertRaises(IntegrityError):
                self.AssignmentType.create({
                    'name': 'Type 2',
                    'code': 'UNIQUE_T001'
                })

    def test_03_type_selection(self):
        """Test assign_type selection field"""
        type_att = self.AssignmentType.create({
            'name': 'Attendance Assignment',
            'code': 'ATT01',
            'assign_type': 'attendance'
        })
        self.assertEqual(type_att.assign_type, 'attendance')
