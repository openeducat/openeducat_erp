# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
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
from odoo.tests import common


class TestAttendanceCommon(common.SavepointCase):
    def setUp(self):
        super(TestAttendanceCommon, self).setUp()
        self.op_attendance_register = self.env['op.attendance.register']
        self.op_attendance_sheet = self.env['op.attendance.sheet']
        self.op_attendance_line = self.env['op.attendance.line']
        self.op_attendance_import = self.env['op.all.student']
        self.op_attendance_wizard = self.env['student.attendance']
