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

from .test_activity_common import TestActivityCommon
from odoo.exceptions import ValidationError
from odoo import fields


class TestActivity(TestActivityCommon):

    def setUp(self):
        super(TestActivity, self).setUp()

    def test_01_activity_functional(self):
        """ Test Activity creation and student integration """
        activity = self.op_activity.create({
            'student_id': self.student.id,
            'faculty_id': self.faculty.id,
            'type_id': self.type_migration.id,
            'description': 'Student Activity Description',
            'date': fields.Date.today(),
        })
        self.assertTrue(activity.id)
        self.assertEqual(activity.student_id, self.student)

        # Check student side
        self.student._compute_count()
        self.assertEqual(self.student.activity_count, 1)
        self.assertIn(activity, self.student.activity_log)

        # Check get_activity action
        action = self.student.get_activity()
        self.assertEqual(action.get('res_model'), 'op.activity')
        self.assertEqual(action.get('domain'), [('student_id', 'in', self.student.ids)])

    def test_02_faculty_default(self):
        """ Test default faculty behavior """
        # Create an activity with faculty user session
        activity = self.op_activity.with_user(self.faculty_user).create({
            'student_id': self.student.id,
            'type_id': self.type_migration.id,
        })
        # The default faculty should match the one linked to faculty_user
        self.assertEqual(activity.faculty_id, self.faculty)


class TestActivityType(TestActivityCommon):

    def setUp(self):
        super(TestActivityType, self).setUp()

    def test_01_activity_type_uniqueness(self):
        """ Test creation of activity type """
        new_type = self.op_activity_type.create({'name': 'Sports Activity'})
        self.assertTrue(new_type.id)


class TestStudentMigrateWizard(TestActivityCommon):

    def setUp(self):
        super(TestStudentMigrateWizard, self).setUp()

    def test_01_migrate_forward_new_course(self):
        """ Test student migration forward to a new course """
        # Ensure we have a valid batch for target course
        batch_3 = self.env['op.batch'].create({
            'name': 'Batch 3',
            'code': 'B3',
            'course_id': self.course_3.id,
            'start_date': '2025-01-01',
            'end_date': '2025-12-31'
        })

        wizard = self.op_student_migrate_wizard.create({
            'course_from_id': self.course_2.id,
            'course_to_id': self.course_3.id,
            'batch_id': batch_3.id,
            'student_ids': [(6, 0, self.student.ids)],
            'course_completed': False,
        })

        wizard.student_migrate_forward()

        # Verify student enrollment change
        enrollment = self.env['op.student.course'].search([
            ('student_id', '=', self.student.id),
            ('course_id', '=', self.course_2.id)
        ])
        self.assertEqual(enrollment.state, 'finished')

        new_enrollment = self.env['op.student.course'].search([
            ('student_id', '=', self.student.id),
            ('course_id', '=', self.course_3.id)
        ])
        self.assertTrue(new_enrollment)

        # Check activity log entry
        self.student._compute_count()
        self.assertGreaterEqual(self.student.activity_count, 1)
        last_activity = self.student.activity_log[-1]
        self.assertIn('Migration from Course 2 to Course 3', last_activity.description)

    def test_02_migrate_completed(self):
        """ Test student migration with course completion """
        wizard = self.op_student_migrate_wizard.create({
            'course_from_id': self.course_2.id,
            'student_ids': [(6, 0, self.student.ids)],
            'course_completed': True,
        })

        wizard.student_migrate_forward()

        enrollment = self.env['op.student.course'].search([
            ('student_id', '=', self.student.id),
            ('course_id', '=', self.course_2.id)
        ])
        self.assertEqual(enrollment.state, 'finished')

    def test_03_migrate_constraint(self):
        """ Test validation error when from course == to course """
        # Test basic create with invalid courses
        with self.assertRaises(ValidationError):
            self.op_student_migrate_wizard.create({
                'course_from_id': self.course_2.id,
                'course_to_id': self.course_2.id,
                'student_ids': [(6, 0, self.student.ids)],
            })

    def test_04_migrate_parent_mismatch(self):
        """ Test validation error when parents don't match """
        course_5 = self.env['op.course'].create({'name': 'Course 5', 'code': 'C5'})
        course_4 = self.env['op.course'].create({
            'name': 'Course 4',
            'code': 'C4',
            'parent_id': course_5.id
        })
        
        with self.assertRaises(ValidationError) as e:
            self.op_student_migrate_wizard.create({
                'course_from_id': self.course_2.id,
                'course_to_id': course_4.id,
                'student_ids': [(6, 0, self.student.ids)],
            })
        self.assertIn("don't share same parent course", str(e.exception))

    def test_05_migrate_proceed_new_admission(self):
        """ Test validation error when course has no parent/program """
        with self.assertRaises(ValidationError) as e:
            self.op_student_migrate_wizard.create({
                'course_from_id': self.course_1.id,
                'course_to_id': self.course_2.id,
                'student_ids': [(6, 0, self.student.ids)],
            })
        self.assertIn("Proceed for new admission", str(e.exception))

    def test_06_compute_methods(self):
        """ Test compute methods for domains """
        wizard = self.env['student.migrate'].new({
            'course_from_id': self.course_2.id
        })
        wizard._compute_student_domain()
        wizard._compute_valid_to_courses()
        
        self.assertIn(self.student._origin.id, wizard.student_ids_domain.ids)
        self.assertIn(self.course_3._origin.id, wizard.valid_to_course_ids.ids)
