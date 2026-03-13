###############################################################################
#
#    openEMIS
#    Copyright (C) 2009-TODAY openEMIS(<https://www.openemis.org>).
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

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestMentorship(TransactionCase):
    """Basic unit tests for the Mentorship module."""

    def setUp(self):
        super(TestMentorship, self).setUp()
        partner_m = self.env['res.partner'].create({'name': 'Mentor Person'})
        self.mentor = self.env['op.mentor'].create({
            'partner_id': partner_m.id,
            'mentor_type': 'professional',
            'profession': 'Engineer',
        })
        partner_s = self.env['res.partner'].create({'name': 'Student Person'})
        self.student = self.env['op.student'].create({
            'first_name': 'Student',
            'last_name': 'Test',
            'gender': 'f',
            'partner_id': partner_s.id,
            'gr_no': 'TST-MNT-001',
        })

    def test_mentor_initial_state(self):
        self.assertEqual(self.mentor.state, 'pending')

    def test_mentor_approve(self):
        self.mentor.action_approve()
        self.assertEqual(self.mentor.state, 'approved')
        self.assertTrue(self.mentor.approval_date)

    def test_mentor_suspend(self):
        self.mentor.action_approve()
        self.mentor.action_suspend()
        self.assertEqual(self.mentor.state, 'suspended')

    def test_direct_message_requires_mentor(self):
        with self.assertRaises(UserError):
            self.env['op.mentorship.message'].create({
                'student_id': self.student.id,
                'message_type': 'direct_message',
                'subject_line': 'Help needed',
                'body': 'Can you help me with maths?',
                # mentor_id intentionally omitted
            })

    def test_group_question_requires_group(self):
        with self.assertRaises(UserError):
            self.env['op.mentorship.message'].create({
                'student_id': self.student.id,
                'message_type': 'group_question',
                'subject_line': 'What is gravity?',
                'body': 'Please explain gravity.',
                # group_id intentionally omitted
            })

    def test_valid_direct_message(self):
        self.mentor.action_approve()
        msg = self.env['op.mentorship.message'].create({
            'student_id': self.student.id,
            'mentor_id': self.mentor.id,
            'message_type': 'direct_message',
            'subject_line': 'Help needed',
            'body': 'Can you help me with maths?',
        })
        self.assertEqual(msg.state, 'open')
        msg.action_mark_answered()
        self.assertEqual(msg.state, 'answered')
