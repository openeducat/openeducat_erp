# -*- coding: utf-8 -*-
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech Receptives(<http://www.techreceptives.com>).
#
##############################################################################

from logging import info
from .test_assignment_common import TestAssignmentCommon


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
            'course_id': self.env.ref('openeducat_core.op_course_4').id,
            'batch_id': self.env.ref('openeducat_core.op_batch_3').id,
            'subject_id': self.env.ref('openeducat_core.op_subject_10').id,
            'faculty_id': self.env.ref('openeducat_core.op_faculty_2').id,
            'submission_date': '2019-12-30',
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
