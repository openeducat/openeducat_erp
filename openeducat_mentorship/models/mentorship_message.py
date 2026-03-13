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

from odoo import _, api, fields, models
from odoo.exceptions import UserError

MESSAGE_TYPES = [
    ('direct_message', 'Direct Message (DM)'),
    ('group_question', 'Group Question'),
    ('group_answer', 'Group Answer'),
]

MESSAGE_STATES = [
    ('open', 'Open'),
    ('answered', 'Answered'),
    ('closed', 'Closed'),
]


class OpMentorshipMessage(models.Model):
    """Represents a direct message from a student to a mentor, or a question
    posted in a mentorship group, or a mentor's answer to a group question."""

    _name = 'op.mentorship.message'
    _description = 'Mentorship Message'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    student_id = fields.Many2one(
        'op.student', string='Student',
        ondelete='cascade', tracking=True, index=True)
    mentor_id = fields.Many2one(
        'op.mentor', string='Mentor',
        ondelete='set null', tracking=True,
        domain=[('state', '=', 'approved')],
        help="Populated for DMs and for answers in group discussions")
    group_id = fields.Many2one(
        'op.mentorship.group', string='Group',
        ondelete='cascade', tracking=True,
        help="Populated for group questions and answers")
    subject_id = fields.Many2one(
        'op.subject', string='Subject / Topic',
        ondelete='set null')
    message_type = fields.Selection(
        MESSAGE_TYPES, string='Type', required=True,
        default='direct_message', tracking=True)
    state = fields.Selection(
        MESSAGE_STATES, string='Status', default='open',
        tracking=True)
    subject_line = fields.Char('Subject Line', required=True)
    body = fields.Text('Message / Question', required=True)
    ai_category_tags = fields.Char(
        'AI Suggested Tags',
        help="Comma-separated tags automatically detected from the "
             "message content by an AI layer")
    parent_id = fields.Many2one(
        'op.mentorship.message', string='Replying To',
        ondelete='set null',
        help="Set when this record is an answer to a group question")
    reply_ids = fields.One2many(
        'op.mentorship.message', 'parent_id',
        string='Answers / Replies')
    reply_count = fields.Integer(
        'Replies', compute='_compute_reply_count', store=True)

    @api.depends('reply_ids')
    def _compute_reply_count(self):
        for rec in self:
            rec.reply_count = len(rec.reply_ids)

    @api.constrains('message_type', 'mentor_id', 'group_id')
    def _check_recipients(self):
        for rec in self:
            if rec.message_type == 'direct_message' and not rec.mentor_id:
                raise UserError(
                    _("A Direct Message must have a Mentor recipient."))
            if rec.message_type in (
                    'group_question', 'group_answer') and not rec.group_id:
                raise UserError(
                    _("Group messages must be linked to a Mentorship Group."))

    def action_mark_answered(self):
        self.write({'state': 'answered'})

    def action_close(self):
        self.write({'state': 'closed'})

    def action_reopen(self):
        self.write({'state': 'open'})

    @api.model
    def _suggest_mentors_for_question(self, subject_id):
        """Return approved mentors who have the given subject in their
        expertise list.  This is called by the UI / AI layer to auto-suggest
        a recipient."""
        return self.env['op.mentor'].search([
            ('state', '=', 'approved'),
            ('expertise_subject_ids', 'in', [subject_id]),
        ])
