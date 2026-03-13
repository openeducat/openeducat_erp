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

AUTHOR_TYPES = [
    ('mentor', 'Mentor'),
    ('teacher', 'Teacher'),
    ('parent', 'Parent'),
    ('professional', 'Professional'),
    ('admin', 'Administrator'),
]

POST_STATES = [
    ('draft', 'Draft'),
    ('review', 'Under Review'),
    ('published', 'Published'),
    ('archived', 'Archived'),
]

CBC_GRADES = [
    ('all', 'All Grades'),
    ('grade_1', 'Grade 1'),
    ('grade_2', 'Grade 2'),
    ('grade_3', 'Grade 3'),
    ('grade_4', 'Grade 4'),
    ('grade_5', 'Grade 5'),
    ('grade_6', 'Grade 6'),
    ('grade_7', 'Grade 7'),
    ('grade_8', 'Grade 8'),
    ('grade_9', 'Grade 9'),
    ('grade_10', 'Grade 10'),
    ('grade_11', 'Grade 11'),
    ('grade_12', 'Grade 12'),
    ('college', 'College / University'),
]


class OpBlogPost(models.Model):
    """An educational blog post authored by a mentor, teacher, parent or
    professional.  Published posts are readable by all students."""

    _name = 'op.blog.post'
    _description = 'Educational Blog Post'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'publish_date desc, name'

    name = fields.Char('Title', required=True, tracking=True)
    slug = fields.Char(
        'URL Slug', index=True,
        help="Short, URL-friendly version of the title")
    author_id = fields.Many2one(
        'res.partner', string='Author', required=True,
        default=lambda self: self.env.user.partner_id, tracking=True)
    author_type = fields.Selection(
        AUTHOR_TYPES, string='Author Type', required=True,
        default='teacher', tracking=True)
    category_ids = fields.Many2many(
        'op.blog.category', string='Categories')
    subject_ids = fields.Many2many(
        'op.subject', string='Related Subjects')
    grade_level = fields.Selection(
        CBC_GRADES, string='Target Grade Level', default='all')
    tags = fields.Char(
        'Tags', help="Comma-separated keyword tags")
    summary = fields.Text(
        'Summary / Excerpt',
        help="Short teaser shown in article listings")
    body = fields.Html(
        'Article Content', required=True,
        sanitize=True)
    cover_image = fields.Binary('Cover Image')
    cover_image_filename = fields.Char('Cover Image Filename')
    state = fields.Selection(
        POST_STATES, string='Status', default='draft',
        tracking=True)
    publish_date = fields.Datetime(
        'Published On', readonly=True, tracking=True)
    view_count = fields.Integer('Views', default=0, readonly=True)
    comment_ids = fields.One2many(
        'op.blog.comment', 'post_id', string='Comments')
    comment_count = fields.Integer(
        'Comments', compute='_compute_comment_count', store=True)
    allow_comments = fields.Boolean(
        'Allow Comments', default=True)
    active = fields.Boolean(default=True)

    @api.depends('comment_ids')
    def _compute_comment_count(self):
        for rec in self:
            rec.comment_count = len(rec.comment_ids)

    @api.constrains('slug')
    def _check_slug_unique(self):
        for rec in self:
            if rec.slug:
                duplicate = self.search([
                    ('slug', '=', rec.slug),
                    ('id', '!=', rec.id),
                ], limit=1)
                if duplicate:
                    raise ValidationError(
                        _("A blog post with slug '%s' already exists.") % rec.slug)

    @api.onchange('name')
    def _onchange_name_slug(self):
        if self.name and not self.slug:
            self.slug = self.name.lower().replace(' ', '-')

    def action_submit_review(self):
        self.write({'state': 'review'})

    def action_publish(self):
        self.write({
            'state': 'published',
            'publish_date': fields.Datetime.now(),
        })

    def action_archive_post(self):
        self.write({'state': 'archived'})

    def action_reset_draft(self):
        self.write({'state': 'draft'})

    def action_increment_views(self):
        for rec in self:
            rec.view_count += 1
