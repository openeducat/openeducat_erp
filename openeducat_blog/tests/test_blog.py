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

from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import TransactionCase


class TestBlog(TransactionCase):
    """Basic unit tests for the Blog module."""

    def setUp(self):
        super(TestBlog, self).setUp()
        self.category = self.env['op.blog.category'].create({
            'name': 'Test Category',
        })

    def test_blog_post_lifecycle(self):
        post = self.env['op.blog.post'].create({
            'name': 'Test Post',
            'author_type': 'teacher',
            'body': '<p>Test content</p>',
            'category_ids': [(4, self.category.id)],
        })
        self.assertEqual(post.state, 'draft')
        post.action_submit_review()
        self.assertEqual(post.state, 'review')
        post.action_publish()
        self.assertEqual(post.state, 'published')
        self.assertTrue(post.publish_date)

    def test_blog_post_slug_generated(self):
        post = self.env['op.blog.post'].new({'name': 'My Test Article'})
        post._onchange_name_slug()
        self.assertEqual(post.slug, 'my-test-article')

    def test_blog_post_slug_unique(self):
        self.env['op.blog.post'].create({
            'name': 'Unique Post',
            'slug': 'unique-post',
            'author_type': 'teacher',
            'body': '<p>Content</p>',
        })
        with self.assertRaises(ValidationError):
            self.env['op.blog.post'].create({
                'name': 'Another Post',
                'slug': 'unique-post',
                'author_type': 'mentor',
                'body': '<p>Content</p>',
            })

    def test_comment_allowed(self):
        post = self.env['op.blog.post'].create({
            'name': 'Commentable Post',
            'author_type': 'teacher',
            'body': '<p>Content</p>',
            'allow_comments': True,
            'state': 'published',
        })
        comment = self.env['op.blog.comment'].create({
            'post_id': post.id,
            'body': 'Great article!',
        })
        self.assertEqual(comment.state, 'pending')
        comment.action_approve()
        self.assertEqual(comment.state, 'approved')

    def test_comment_not_allowed(self):
        post = self.env['op.blog.post'].create({
            'name': 'No Comment Post',
            'author_type': 'teacher',
            'body': '<p>Content</p>',
            'allow_comments': False,
            'state': 'published',
        })
        with self.assertRaises(UserError):
            self.env['op.blog.comment'].create({
                'post_id': post.id,
                'body': 'Trying to comment',
            })
