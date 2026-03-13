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


class OpBlogCategory(models.Model):
    """Hierarchical category for blog posts.  Top-level categories group
    posts by educational theme (e.g. STEM, Health, Career Guidance); children
    can refine by grade band or subject."""

    _name = 'op.blog.category'
    _description = 'Blog Category'
    _order = 'name'

    name = fields.Char('Category Name', required=True)
    description = fields.Text('Description')
    parent_id = fields.Many2one(
        'op.blog.category', string='Parent Category',
        ondelete='set null', index=True)
    child_ids = fields.One2many(
        'op.blog.category', 'parent_id', string='Sub-Categories')
    post_count = fields.Integer(
        'Posts', compute='_compute_post_count')
    active = fields.Boolean(default=True)

    def _compute_post_count(self):
        for rec in self:
            rec.post_count = self.env['op.blog.post'].search_count([
                ('category_ids', 'in', [rec.id]),
                ('state', '=', 'published'),
            ])
