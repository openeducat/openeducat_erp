# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
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


class TestTimetableCommon(common.TransactionCase):
    def setUp(self):
        super(TestTimetableCommon, self).setUp()
        self.op_faculty = self.env['op.faculty']
        self.op_session = self.env['op.session']
        self.op_timing = self.env['op.timing']
        self.generate_timetable = self.env['generate.time.table']
        self.wizard_session = self.env['gen.time.table.line']
        self.timetable_report = self.env['time.table.report']
