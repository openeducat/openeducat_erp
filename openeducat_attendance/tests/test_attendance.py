# -*- coding: utf-8 -*-
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

from logging import info
import time
from .test_attendance_common import TestAttendanceCommon


class TestAttendanceRegister(TestAttendanceCommon):

    def setUp(self):
        super(TestAttendanceRegister, self).setUp()

    def test_case_attendance_register(self):
        register = self.op_attendance_register.search([])
        for record in register:
            info('      Attendance Register : %s' % record.name)
            info('      Course : %s' % record.course_id.name)
            info('      Code : %s' % record.code)


class TestAttendanceSheet(TestAttendanceCommon):

    def setUp(self):
        super(TestAttendanceSheet, self).setUp()

    def test_case_attendance_sheet(self):
        sheet = self.op_attendance_sheet.create({
            'name': 'AS',
            'attendance_date': time.strftime('%Y-%m-01'),
            'register_id':
                self.env.ref('openeducat_attendance.'
                             'op_attendance_register_1').id
        })
        info('  Details Of Attendance Sheet:.....')
        for record in sheet:
            record.attendance_draft()
            record.attendance_start()
            record.attendance_done()
            record.attendance_cancel()


class TestAttendanceLine(TestAttendanceCommon):

    def setUp(self):
        super(TestAttendanceLine, self).setUp()

    def test_case_attendance_line(self):
        line = self.op_attendance_line.search([])
        info('  Details Of Attendance Lines:.....')
        for record in line:
            info('      Attendance Sheet : %s' % record.attendance_id.name)
            info('      Student : %s' % record.student_id.name)
            info('      Register : %s' % record.register_id.name)
            info('      Present : %s' % record.present)


class TestAttendanceWizard(TestAttendanceCommon):

    def setUp(self):
        super(TestAttendanceWizard, self).setUp()

    def test_case_attendance_wizard(self):
        student = self.op_attendance_wizard.create({
            'from_date': time.strftime('%Y-%m-01'),
            'to_date': time.strftime('%Y-%m-01')
        })
        student.print_report()
