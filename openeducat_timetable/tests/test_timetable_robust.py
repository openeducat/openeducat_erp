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

from odoo.tests import TransactionCase, tagged
from odoo.exceptions import ValidationError
from odoo import fields
import datetime


@tagged('post_install', '-at_install')
class TestTimetableRobustCommon(TransactionCase):
    def setUp(self):
        super(TestTimetableRobustCommon, self).setUp()
        self.Course = self.env['op.course']
        self.Batch = self.env['op.batch']
        self.Faculty = self.env['op.faculty']
        self.Subject = self.env['op.subject']
        self.Session = self.env['op.session']
        self.Timing = self.env['op.timing']
        self.Classroom = self.env['op.classroom']

        # Academic Basics
        self.course = self.Course.create({'name': 'Timetable Course', 'code': 'TTC'})
        self.subject = self.Subject.create({'name': 'Timetable Subject', 'code': 'TTS'})
        self.course.subject_ids = [(6, 0, [self.subject.id])]
        
        self.batch = self.Batch.create({
            'name': 'TT Batch', 'code': 'TTB', 'course_id': self.course.id,
            'start_date': fields.Date.today(),
            'end_date': fields.Date.today() + datetime.timedelta(days=30)
        })

        # Faculty
        self.faculty_user = self.env['res.users'].create({
            'name': 'TT Faculty', 'login': 'tt_fac', 'email': 'tt@test.com',
            'group_ids': [(6, 0, [self.env.ref('base.group_user').id])]
        })
        self.faculty = self.Faculty.create({
            'first_name': 'TT', 'last_name': 'Fac', 'gender': 'male',
            'birth_date': '1985-01-01', 'user_id': self.faculty_user.id
        })

        # Timing
        self.timing = self.Timing.create({
            'name': 'Morning Slot', 'hour': '9', 'minute': '00', 'am_pm': 'am'
        })
        
        # Classroom
        self.classroom = self.Classroom.create({
            'name': 'Room 101', 
            'code': 'R101',
            'capacity': 30
        })


class TestTimingModel(TestTimetableRobustCommon):
    """3 tests for op.timing"""

    def test_01_timing_creation(self):
        """Standard timing creation"""
        t = self.Timing.create({'name': 'Evening', 'hour': '5', 'minute': '30', 'am_pm': 'pm'})
        self.assertTrue(t.id)

    def test_02_timing_sequence(self):
        """Check if sequence is working (default 0)"""
        t = self.Timing.create({'name': 'Seq Test', 'hour': '10', 'minute': '00', 'am_pm': 'am'})
        self.assertEqual(t.sequence, 0)

    def test_03_timing_name(self):
        """Check name is set correctly"""
        self.assertEqual(self.timing.name, 'Morning Slot')


class TestSessionModel(TestTimetableRobustCommon):
    """3 tests for op.session"""

    def test_01_session_creation_and_computed_name(self):
        """Verify session name includes faculty, subject and time"""
        start = fields.Datetime.now()
        end = start + datetime.timedelta(hours=1)
        session = self.Session.create({
            'faculty_id': self.faculty.id,
            'subject_id': self.subject.id,
            'course_id': self.course.id,
            'batch_id': self.batch.id,
            'start_datetime': start,
            'end_datetime': end,
            'timing_id': self.timing.id
        })
        self.assertIn('TT Fac', session.name)
        self.assertIn('Timetable Subject', session.name)

    def test_02_date_validation(self):
        """Verify end time cannot be before start time"""
        start = fields.Datetime.now()
        end = start - datetime.timedelta(hours=1)
        with self.assertRaises(ValidationError):
            self.Session.create({
                'faculty_id': self.faculty.id,
                'subject_id': self.subject.id,
                'course_id': self.course.id,
                'batch_id': self.batch.id,
                'start_datetime': start,
                'end_datetime': end
            })

    def test_03_session_states(self):
        """Verify state transitions: draft -> confirm -> done -> cancel"""
        start = fields.Datetime.now()
        end = start + datetime.timedelta(hours=1)
        session = self.Session.create({
            'faculty_id': self.faculty.id,
            'subject_id': self.subject.id,
            'course_id': self.course.id,
            'batch_id': self.batch.id,
            'start_datetime': start,
            'end_datetime': end
        })
        self.assertEqual(session.state, 'draft')
        session.lecture_confirm()
        self.assertEqual(session.state, 'confirm')
        session.lecture_done()
        self.assertEqual(session.state, 'done')
        session.lecture_cancel()
        self.assertEqual(session.state, 'cancel')


class TestTimetableConflicts(TestTimetableRobustCommon):
    """3 tests for session conflicts (Hard constraints)"""

    def setUp(self):
        super(TestTimetableConflicts, self).setUp()
        # Enable constraints via config parameters
        self.env['ir.config_parameter'].sudo().set_param('timetable.is_faculty_constraint', 'True')
        self.env['ir.config_parameter'].sudo().set_param('timetable.is_classroom_constraint', 'True')
        self.env['ir.config_parameter'].sudo().set_param('timetable.is_batch_constraint', 'True')

    def test_01_faculty_conflict(self):
        """Verify same faculty cannot have two sessions at the same time"""
        dt = fields.Datetime.now().replace(minute=0, second=0, microsecond=0)
        start1 = dt
        end1 = dt + datetime.timedelta(hours=1)
        
        self.Session.create({
            'faculty_id': self.faculty.id,
            'subject_id': self.subject.id,
            'course_id': self.course.id,
            'batch_id': self.batch.id,
            'start_datetime': start1,
            'end_datetime': end1
        })
        
        # Another batch, but same faculty same time
        batch2 = self.Batch.create({
            'name': 'B2', 
            'code': 'B2', 
            'course_id': self.course.id,
            'start_date': fields.Date.today(),
            'end_date': fields.Date.today() + datetime.timedelta(days=30)
        })
        with self.assertRaises(ValidationError):
            self.Session.create({
                'faculty_id': self.faculty.id,
                'subject_id': self.subject.id,
                'course_id': self.course.id,
                'batch_id': batch2.id,
                'start_datetime': start1,
                'end_datetime': end1
            })

    def test_02_classroom_conflict(self):
        """Verify same classroom cannot be used twice at the same time"""
        dt = fields.Datetime.now().replace(minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
        start1 = dt
        end1 = dt + datetime.timedelta(hours=1)
        
        faculty2 = self.Faculty.create({
            'first_name': 'F2', 'last_name': 'T2', 'gender': 'male', 'birth_date': '1990-01-01'
        })
        
        self.Session.create({
            'faculty_id': self.faculty.id,
            'subject_id': self.subject.id,
            'course_id': self.course.id,
            'batch_id': self.batch.id,
            'start_datetime': start1,
            'end_datetime': end1,
            'classroom_id': self.classroom.id
        })
        
        with self.assertRaises(ValidationError):
            self.Session.create({
                'faculty_id': faculty2.id,
                'subject_id': self.subject.id,
                'course_id': self.course.id,
                'batch_id': self.batch.id,
                'start_datetime': start1,
                'end_datetime': end1,
                'classroom_id': self.classroom.id
            })

    def test_03_batch_conflict(self):
        """Verify same batch cannot have two sessions at the same time"""
        dt = fields.Datetime.now().replace(minute=0, second=0, microsecond=0) + datetime.timedelta(days=2)
        start1 = dt
        end1 = dt + datetime.timedelta(hours=1)
        
        faculty2 = self.Faculty.create({
            'first_name': 'F3', 'last_name': 'T3', 'gender': 'male', 'birth_date': '1990-01-01'
        })
        
        self.Session.create({
            'faculty_id': self.faculty.id,
            'subject_id': self.subject.id,
            'course_id': self.course.id,
            'batch_id': self.batch.id,
            'start_datetime': start1,
            'end_datetime': end1
        })
        
        with self.assertRaises(ValidationError):
            self.Session.create({
                'faculty_id': faculty2.id,
                'subject_id': self.subject.id,
                'course_id': self.course.id,
                'batch_id': self.batch.id,
                'start_datetime': start1,
                'end_datetime': end1
            })
