# -*- coding: utf-8 -*-
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech Receptives(<http://www.techreceptives.com>).
#
##############################################################################

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
