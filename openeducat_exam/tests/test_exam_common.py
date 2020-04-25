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


class TestExamCommon(common.SavepointCase):
    def setUp(self):
        super(TestExamCommon, self).setUp()
        self.op_exam = self.env['op.exam']
        self.op_exam_attendees = self.env['op.exam.attendees']
        self.op_exam_room = self.env['op.exam.room']
        self.op_exam_session = self.env['op.exam.session']
        self.op_exam_type = self.env['op.exam.type']
        self.op_grade_configuration = self.env['op.grade.configuration']
        self.op_marksheet_line = self.env['op.marksheet.line']
        self.op_marksheet_register = self.env['op.marksheet.register']
        self.op_res_partner = self.env['res.partner']
        self.op_result_line = self.env['op.result.line']
        self.op_result_template = self.env['op.result.template']
        self.op_held_exam = self.env['op.held.exam']
        self.op_room_distribution = self.env['op.room.distribution']
        self.student_hall_ticket = self.env['student.hall.ticket']
