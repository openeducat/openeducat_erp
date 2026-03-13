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
from odoo.exceptions import ValidationError

MENTOR_TYPES = [
    ('professional', 'Professional'),
    ('teacher', 'Teacher'),
    ('parent', 'Parent'),
]

MENTOR_STATES = [
    ('pending', 'Pending Approval'),
    ('approved', 'Approved'),
    ('suspended', 'Suspended'),
    ('rejected', 'Rejected'),
]


class OpMentor(models.Model):
    """A mentor is any approved adult (professional, teacher or parent) who
    has registered on the platform and been approved to guide students."""

    _name = 'op.mentor'
    _description = 'Mentor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    partner_id = fields.Many2one(
        'res.partner', string='Contact', required=True,
        ondelete='cascade', tracking=True)
    name = fields.Char(
        'Full Name', related='partner_id.name', store=True, readonly=False)
    email = fields.Char(
        'Email', related='partner_id.email', store=True, readonly=False)
    phone = fields.Char(
        'Phone', related='partner_id.phone', store=True, readonly=False)
    mentor_type = fields.Selection(
        MENTOR_TYPES, string='Mentor Type', required=True,
        default='professional', tracking=True)
    state = fields.Selection(
        MENTOR_STATES, string='Status', default='pending',
        tracking=True)
    profession = fields.Char('Profession / Role')
    bio = fields.Text('Bio / Profile')
    expertise_subject_ids = fields.Many2many(
        'op.subject', string='Areas of Expertise',
        help="Subjects or topics the mentor specialises in")
    approved_by = fields.Many2one(
        'res.users', string='Approved By', readonly=True, tracking=True)
    approval_date = fields.Datetime(
        'Approval Date', readonly=True, tracking=True)
    active = fields.Boolean(default=True)
    message_count = fields.Integer(
        'DM Count', compute='_compute_message_count')
    group_ids = fields.Many2many(
        'op.mentorship.group',
        'op_mentor_group_rel',
        'mentor_id', 'group_id',
        string='Mentorship Groups')

    @api.depends('partner_id')
    def _compute_message_count(self):
        for rec in self:
            rec.message_count = self.env['op.mentorship.message'].search_count([
                ('mentor_id', '=', rec.id)])

    def action_approve(self):
        for rec in self:
            if rec.state != 'approved':
                rec.write({
                    'state': 'approved',
                    'approved_by': self.env.uid,
                    'approval_date': fields.Datetime.now(),
                })
        return True

    def action_suspend(self):
        self.write({'state': 'suspended'})

    def action_reject(self):
        self.write({'state': 'rejected'})

    def action_reset_pending(self):
        self.write({'state': 'pending'})

    @api.constrains('state')
    def _check_approval(self):
        for rec in self:
            if rec.state == 'approved' and not rec.partner_id:
                raise ValidationError(
                    _("A contact must be linked before approving a mentor."))
