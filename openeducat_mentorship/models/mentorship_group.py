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

from odoo import fields, models


class OpMentorshipGroup(models.Model):
    """A group discussion space where students post questions and mentors
    who have expertise in the relevant subjects respond."""

    _name = 'op.mentorship.group'
    _description = 'Mentorship Group'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char('Group Name', required=True)
    description = fields.Text('Description')
    subject_ids = fields.Many2many(
        'op.subject', string='Related Subjects',
        help="Subjects covered by this group – used for question routing")
    mentor_ids = fields.Many2many(
        'op.mentor',
        'op_mentor_group_rel',
        'group_id', 'mentor_id',
        string='Mentors',
        domain=[('state', '=', 'approved')])
    student_ids = fields.Many2many(
        'op.student', string='Enrolled Students')
    is_open = fields.Boolean(
        'Open for All Students?', default=True,
        help="If checked, any student can join; otherwise students are "
             "added individually.")
    question_ids = fields.One2many(
        'op.mentorship.message', 'group_id',
        string='Questions',
        domain=[('message_type', '=', 'group_question')])
    question_count = fields.Integer(
        'Questions', compute='_compute_question_count')
    active = fields.Boolean(default=True)

    def _compute_question_count(self):
        for rec in self:
            rec.question_count = len(rec.question_ids)
