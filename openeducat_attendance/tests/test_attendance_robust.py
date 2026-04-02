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
from odoo.exceptions import ValidationError
from odoo import fields
import datetime


class TestAttendanceRobustCommon(TransactionCase):
    def setUp(self):
        super(TestAttendanceRobustCommon, self).setUp()
        self.Course = self.env['op.course']
        self.Batch = self.env['op.batch']
        self.Faculty = self.env['op.faculty']
        self.Student = self.env['op.student']
        self.Register = self.env['op.attendance.register']
        self.Sheet = self.env['op.attendance.sheet']
        self.Line = self.env['op.attendance.line']
        self.Subject = self.env['op.subject']
        self.Session = self.env['op.session']

        # Academic Setup
        self.course = self.Course.create({'name': 'Test Course', 'code': 'TC'})
        self.subject = self.Subject.create({'name': 'Test Subject', 'code': 'TS'})
        self.batch = self.Batch.create({
            'name': 'Test Batch', 
            'code': 'TB', 
            'course_id': self.course.id,
            'start_date': fields.Date.today(),
            'end_date': fields.Date.today() + datetime.timedelta(days=30)
        })
        
        # Faculty & Student
        self.faculty_user = self.env['res.users'].create({
            'name': 'Fac User', 'login': 'fac_user_att', 'email': 'att_f@test.com',
            'group_ids': [(6, 0, [self.env.ref('base.group_user').id])]
        })
        self.faculty = self.Faculty.create({
            'first_name': 'Fac', 'last_name': 'Test', 'gender': 'male',
            'birth_date': '1990-01-01', 'user_id': self.faculty_user.id
        })
        
        self.student = self.Student.create({
            'first_name': 'Stu', 'last_name': 'Test', 'gender': 'm',
            'birth_date': '2010-01-01'
        })


class TestAttendanceRegister(TestAttendanceRobustCommon):
    """3 tests for op.attendance.register"""

    def test_01_register_creation(self):
        """Simple register creation and field checks"""
        reg = self.Register.create({
            'name': 'Autumn 2026',
            'code': 'ATT-001',
            'course_id': self.course.id,
            'batch_id': self.batch.id
        })
        self.assertTrue(reg.id)
        self.assertEqual(reg.code, 'ATT-001')

    def test_02_register_unique_code(self):
        """Test unique code constraint on register"""
        from psycopg2 import IntegrityError
        from odoo.tools import mute_logger
        
        self.Register.create({
            'name': 'Reg 1', 'code': 'DUPE-CODE', 'course_id': self.course.id, 'batch_id': self.batch.id
        })
        with self.cr.savepoint(), mute_logger('odoo.sql_db'):
            with self.assertRaises(IntegrityError):
                self.Register.create({
                    'name': 'Reg 2', 'code': 'DUPE-CODE', 'course_id': self.course.id, 'batch_id': self.batch.id
                })

    def test_03_register_activation(self):
        """Test archive/unarchive behavior"""
        reg = self.Register.create({
            'name': 'Temp Reg', 'code': 'TEMP-01', 'course_id': self.course.id, 'batch_id': self.batch.id
        })
        self.assertTrue(reg.active)
        reg.active = False
        self.assertFalse(reg.active)


class TestAttendanceSheet(TestAttendanceRobustCommon):
    """3 tests for op.attendance.sheet"""

    def setUp(self):
        super(TestAttendanceSheet, self).setUp()
        self.reg = self.Register.create({
            'name': 'Main Reg', 'code': 'MAIN-01', 'course_id': self.course.id, 'batch_id': self.batch.id
        })

    def test_01_sheet_creation_and_sequence(self):
        """Validates sheet name is correctly generated from Register code + Sequence"""
        sheet = self.Sheet.create({
            'register_id': self.reg.id,
            'attendance_date': fields.Date.today(),
            'faculty_id': self.faculty.id
        })
        self.assertTrue(sheet.name.startswith('MAIN-01'))

    def test_02_sheet_states(self):
        """Transitions: draft -> start -> done -> cancel"""
        sheet = self.Sheet.create({
            'register_id': self.reg.id,
            'attendance_date': fields.Date.today()
        })
        self.assertEqual(sheet.state, 'draft')
        
        sheet.attendance_start()
        self.assertEqual(sheet.state, 'start')
        
        sheet.attendance_done()
        self.assertEqual(sheet.state, 'done')
        
        sheet.attendance_cancel()
        self.assertEqual(sheet.state, 'cancel')

    def test_03_sheet_uniqueness(self):
        """Sheet must be unique per Register/Date/Session"""
        from psycopg2 import IntegrityError
        from odoo.tools import mute_logger
        
        today = fields.Date.today()
        self.Sheet.create({'register_id': self.reg.id, 'attendance_date': today})
        
        with self.cr.savepoint(), mute_logger('odoo.sql_db'):
            with self.assertRaises(IntegrityError):
                self.Sheet.create({'register_id': self.reg.id, 'attendance_date': today})


class TestAttendanceLine(TestAttendanceRobustCommon):
    """3 tests for op.attendance.line"""

    def setUp(self):
        super(TestAttendanceLine, self).setUp()
        self.reg = self.Register.create({
            'name': 'Line Reg', 'code': 'LINE-01', 'course_id': self.course.id, 'batch_id': self.batch.id
        })
        self.sheet = self.Sheet.create({
            'register_id': self.reg.id,
            'attendance_date': fields.Date.today()
        })

    def test_01_line_creation(self):
        """Checks successful record creation for a student"""
        line = self.Line.create({
            'attendance_id': self.sheet.id,
            'student_id': self.student.id,
            'present': True
        })
        self.assertTrue(line.id)
        self.assertEqual(line.state, 'draft')

    def test_02_mutually_exclusive_flags(self):
        """Tests that selecting Present clears Absent, Late, Excused via onchange"""
        # Note: In back-end write(), onchanges don't fire automatically, but we can call them or verify them
        line = self.Line.new({
            'attendance_id': self.sheet.id,
            'student_id': self.student.id,
            'absent': True
        })
        self.assertTrue(line.absent)
        
        # Mark as present
        line.present = True
        line.onchange_present()
        self.assertFalse(line.absent)
        self.assertFalse(line.late)

    def test_03_duplicate_student_on_sheet(self):
        """Ensures the same student cannot be marked twice on the same sheet"""
        from psycopg2 import IntegrityError
        from odoo.tools import mute_logger
        
        self.Line.create({
            'attendance_id': self.sheet.id, 'student_id': self.student.id, 'present': True
        })
        with self.cr.savepoint(), mute_logger('odoo.sql_db'):
            with self.assertRaises(IntegrityError):
                self.Line.create({
                    'attendance_id': self.sheet.id, 'student_id': self.student.id, 'present': False
                })

    def test_04_onchange_methods(self):
        """Tests that selecting Present clears other flags via onchange methods"""
        line = self.Line.new({
            'attendance_id': self.sheet.id,
            'student_id': self.student.id,
            'absent': True
        })
        self.assertTrue(line.absent)
        
        line.present = True
        line.onchange_present()
        self.assertFalse(line.absent)
        self.assertFalse(line.late)
        self.assertFalse(line.excused)

        line.late = True
        line.onchange_late()
        self.assertFalse(line.present)

        line.excused = True
        line.onchange_excused()
        self.assertFalse(line.late)

        line.absent = True
        line.onchange_absent()
        self.assertFalse(line.excused)


class TestAttendanceIntegration(TestAttendanceRobustCommon):
    """Integration tests for Sessions and Reports"""

    def test_01_session_get_attendance(self):
        """Validates get_attendance logic on op.session"""
        session = self.Session.create({
            'name': 'Logic 101',
            'course_id': self.course.id,
            'batch_id': self.batch.id,
            'subject_id': self.subject.id,
            'faculty_id': self.faculty.id,
            'start_datetime': fields.Datetime.now(),
            'end_datetime': fields.Datetime.now() + datetime.timedelta(hours=1)
        })
        
        # Test case: No sheet exists yet
        action = session.get_attendance()
        self.assertEqual(action.get('res_model'), 'op.attendance.sheet')
        self.assertFalse(action.get('res_id'))

        # Test case: Sheet exists
        sheet = self.Sheet.create({
            'register_id': self.Register.create({
                'name': 'Reg', 'code': 'R', 'course_id': self.course.id, 'batch_id': self.batch.id
            }).id,
            'session_id': session.id,
            'attendance_date': fields.Date.today()
        })
        action_loaded = session.get_attendance()
        self.assertEqual(action_loaded.get('res_id'), sheet.id)

    def test_02_report_data_generation(self):
        """Verifies attendance report calculation logic"""
        Report = self.env['report.openeducat_attendance.student_attendance_report']
        
        # Create some attendance data
        reg = self.Register.create({
            'name': 'Rep Reg', 'code': 'RR', 'course_id': self.course.id, 'batch_id': self.batch.id
        })
        sheet = self.Sheet.create({
            'register_id': reg.id,
            'attendance_date': fields.Date.today()
        })
        self.Line.create({
            'attendance_id': sheet.id, 'student_id': self.student.id, 'present': True
        })
        
        data = {
            'student_id': self.student.id,
            'from_date': fields.Date.today(),
            'to_date': fields.Date.today()
        }
        values = Report._get_report_values(docids=[], data=data)
        
        self.assertEqual(values['student'], self.student)
        self.assertEqual(len(values['absences']), 1)
        self.assertEqual(values['absences'][0]['remark'], 'Present')
        self.assertEqual(values['present_count'], 1)
