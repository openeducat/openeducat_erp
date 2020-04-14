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


from odoo.tests import common, TransactionCase
from ..controllers import app_main
from odoo.addons.website.tools import MockRequest


class TestCoreCommon(common.SavepointCase):
    def setUp(self):
        super(TestCoreCommon, self).setUp()
        self.op_batch = self.env['op.batch']
        self.op_faculty = self.env['op.faculty']
        self.op_course = self.env['op.course']
        self.res_company = self.env['res.users']
        self.op_student = self.env['op.student']
        self.hr_emp = self.env['hr.employee']
        self.subject_registration = self.env['op.subject.registration']
        self.op_update = self.env['publisher_warranty.contract']
        self.employ_wizard = self.env['wizard.op.faculty.employee']
        self.faculty_user_wizard = self.env['wizard.op.faculty']
        self.studnet_wizard = self.env['wizard.op.student']
