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

COMMENT_STATES = [
    ('pending', 'Pending Moderation'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]


class OpBlogComment(models.Model):
    """A student (or any authenticated user) can leave a comment on a
    published blog post.  Comments require moderation before appearing."""

    _name = 'op.blog.comment'
    _description = 'Blog Comment'
    _inherit = ['mail.thread']
    _order = 'create_date asc'

    post_id = fields.Many2one(
        'op.blog.post', string='Blog Post', required=True,
        ondelete='cascade', index=True)
    author_id = fields.Many2one(
        'res.partner', string='Author',
        default=lambda self: self.env.user.partner_id,
        ondelete='set null')
    body = fields.Text('Comment', required=True)
    state = fields.Selection(
        COMMENT_STATES, string='Status', default='pending',
        tracking=True)
    parent_id = fields.Many2one(
        'op.blog.comment', string='Reply To',
        ondelete='set null',
        help="Set for nested replies to another comment")
    reply_ids = fields.One2many(
        'op.blog.comment', 'parent_id', string='Replies')

    @api.constrains('post_id')
    def _check_comments_allowed(self):
        for rec in self:
            if not rec.post_id.allow_comments:
                raise UserError(
                    _("Comments are disabled for this blog post."))

    def action_approve(self):
        self.write({'state': 'approved'})

    def action_reject(self):
        self.write({'state': 'rejected'})
