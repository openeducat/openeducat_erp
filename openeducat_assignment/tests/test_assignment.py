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

from logging import info
from .test_assignment_common import TestAssignmentCommon
import time


class TestAssignment(TestAssignmentCommon):

    def setUp(self):
        super(TestAssignment, self).setUp()

    def test_case_assignment(self):
        assignment = self.op_assignment.search([])
        if not assignment:
            raise AssertionError(
                'Error in data, please check for reference Assignment')
        info('Details of Meeting')
        for record in assignment:
            info('      Name : %s' % record.name)
            info('      Course : %s' % record.course_id.id)
            info('      Batch : %s' % record.batch_id.id)
            info('      Subject : %s' % record.subject_id.id)
            info('      Faculty : %s' % record.faculty_id.id)
            info('      Assignment Type : %s' % record.assignment_type_id.id)
            info('      Marks : %s' % record.marks)
            info('      Description : %s' % record.description)
            info('      State : %s' % record.state)
            info('      Issued_date : %s' % record.issued_date)
            info('      Submission_date : %s' % record.submission_date)
            info('      Allocation Ids : %s' % record.allocation_ids.ids)
            info('      Assignments : %s' % record.assignment_sub_line)
            info('      Reviewer : %s' % record.reviewer.id)
            record.onchange_course()
            record.act_publish()
            record.act_finish()
            record.act_cancel()
            record.act_set_to_draft()


class TestAssignmentSubline(TestAssignmentCommon):

    def setUp(self):
        super(TestAssignmentSubline, self).setUp()

    def test_case_assignment_subline(self):
        assignment_subline = self.op_assignment_subline.search([])
        assignment = self.env["op.assignment"].create({
            'name': "LRTP - 001 - Asg - 009",
            'state': "draft",
            'marks': 50,
            'assignment_type_id':
                self.env.ref('openeducat_assignment.op_assignment_type_1').id,
            'issued_date': time.strftime('%Y-%m-01'),
            'course_id': self.env.ref('openeducat_core.op_course_4').id,
            'batch_id': self.env.ref('openeducat_core.op_batch_3').id,
            'subject_id': self.env.ref('openeducat_core.op_subject_10').id,
            'faculty_id': self.env.ref('openeducat_core.op_faculty_2').id,
            'submission_date': time.strftime('%Y-%m-01'),
            'allocation_ids': self.env.ref("openeducat_core.op_student_9"),
            'description': 'Please answer the following questions briefly:'
                           ' - 1. What are the different types of land',
        })
        assignment_subline1 = self.op_assignment_subline.create({
            'assignment_id': assignment.id,
            'state': "draft",
            'student_id': self.env.ref("openeducat_core.op_student_9").id,
            'description': 'The answers of the questions are placed here',
        })
        assignment_subline1.unlink()
        for record in assignment_subline:
            info('      Assignment Name : %s' % record.assignment_id.id)
            info('      Student : %s' % record.student_id.id)
            info('      Description : %s' % record.description)
            info('      State : %s' % record.state)
            info('      submission_date : %s' % record.submission_date)
            info('      Marks : %s' % record.marks)
            info('      Note : %s' % record.note)
            info('      User : %s' % record.user_id.id)
            info('      Faculty : %s' % record.faculty_user_id.id)
            info('      Check User Boolean : %s' % record.user_boolean)
            record.act_draft()
            record.act_submit()
            record.act_accept()
            record.act_change_req()
            record.act_reject()
