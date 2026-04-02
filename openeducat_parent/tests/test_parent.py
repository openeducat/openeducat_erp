###############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<https://www.openeducat.org>).
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

from .test_parent_common import TestParentCommon
from odoo.exceptions import ValidationError, AccessError
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class TestParentModel(TestParentCommon):
    """Test cases for op.parent"""

    def test_01_parent_creation(self):
        parent = self.op_parent.create({
            'name': self.parent_partner.id,
            'relationship_id': self.rel_father.id,
            'student_ids': [(6, 0, [self.student.id])],
        })
        self.assertEqual(parent.name, self.parent_partner)
        self.assertTrue(self.parent_partner.is_parent)
        self.assertIn(self.student, parent.student_ids)

    def test_02_onchange_name(self):
        parent = self.op_parent.new({
            'name': self.parent_partner.id,
        })
        parent._onchange_name()
        self.assertEqual(parent.email, self.parent_partner.email)
        self.assertEqual(parent.mobile, self.parent_partner.phone)

    def test_03_create_parent_user(self):
        # We need a template for user creation
        group_portal = self.env.ref('base.group_portal')
        template_xml_id = 'openeducat_parent.parent_template_user'
        try:
            template_user = self.env.ref(template_xml_id)
        except ValueError:
            template_user = self.env['res.users'].create({
                'name': 'Parent Template Mock',
                'login': 'parent_template_mock',
                'group_ids': [(6, 0, [group_portal.id])]
            })
            self.env['ir.model.data'].create({
                'name': 'parent_template_user',
                'module': 'openeducat_parent',
                'res_id': template_user.id,
                'model': 'res.users',
            })

        parent = self.op_parent.create({
            'name': self.parent_partner.id,
            'relationship_id': self.rel_father.id,
            'student_ids': [(6, 0, [self.student.id])],
        })
        parent.create_parent_user()
        self.assertTrue(parent.user_id)
        self.assertEqual(parent.user_id.partner_id, self.parent_partner)
        self.assertTrue(parent.user_id.is_parent)
        # Verify children link
        if self.student.user_id:
            self.assertIn(self.student.user_id, parent.user_id.child_ids)


@tagged('post_install', '-at_install')
class TestParentRelation(TestParentCommon):
    """Test cases for op.parent.relationship"""

    def test_01_relation_creation(self):
        rel = self.op_parent_relationship.create({'name': 'Brother'})
        self.assertEqual(rel.name, 'Brother')

    def test_02_unique_name(self):
        with self.assertRaises(Exception):
            self.op_parent_relationship.create({'name': 'Test Father'})

    def test_03_relation_search(self):
        rels = self.op_parent_relationship.search([('name', '=', 'Test Mother')])
        self.assertIn(self.rel_mother, rels)


@tagged('post_install', '-at_install')
class TestStudentParent(TestParentCommon):
    """Test cases for op.student parent-related logic"""

    def test_01_student_parent_link(self):
        parent = self.op_parent.create({
            'name': self.parent_partner.id,
            'relationship_id': self.rel_father.id,
            'student_ids': [(6, 0, [self.student.id])],
        })
        self.assertIn(parent, self.student.parent_ids)

    def test_02_student_write_parents(self):
        # Create another parent
        partner2 = self.env['res.partner'].create({'name': 'Parent 2'})
        parent2 = self.op_parent.create({
            'name': partner2.id,
            'relationship_id': self.rel_mother.id,
            'student_ids': [(6, 0, [self.student.id])],
        })
        self.student.write({'parent_ids': [(4, parent2.id)]})
        self.assertIn(parent2, self.student.parent_ids)

    def test_03_get_parent_action(self):
        self.op_parent.create({
            'name': self.parent_partner.id,
            'relationship_id': self.rel_father.id,
            'student_ids': [(6, 0, [self.student.id])],
        })
        action = self.student.get_parent()
        self.assertEqual(action['res_model'], 'op.parent')
        self.assertIn(self.student.id, action['context']['default_student_ids'][0][2])


@tagged('post_install', '-at_install')
class TestSubjectRegistrationParent(TestParentCommon):
    """Test cases for op.subject.registration parent constraints"""

    def test_01_parent_cannot_create_registration(self):
        # Create a parent user
        parent_user = self.env['res.users'].create({
            'name': 'Parent User',
            'login': 'parent_user',
            'group_ids': [(6, 0, [self.env.ref('base.group_portal').id])]
        })
        # Link to student (parent can have child_ids)
        parent_user.child_ids = [(4, self.env.user.id)] # Mocking parent-child link

        with self.assertRaises(Exception):
            self.subject_registration.with_user(parent_user).create({
                'student_id': self.student.id,
                'course_id': self.course.id,
                'batch_id': self.batch.id,
            })

    def test_02_normal_user_can_create_registration(self):
        reg = self.subject_registration.create({
            'student_id': self.student.id,
            'course_id': self.course.id,
            'batch_id': self.batch.id,
        })
        self.assertTrue(reg)

    def test_03_parent_cannot_write_registration(self):
        reg = self.subject_registration.create({
            'student_id': self.student.id,
            'course_id': self.course.id,
            'batch_id': self.batch.id,
        })
        parent_user = self.env['res.users'].create({
            'name': 'Parent User 3',
            'login': 'parent_user_3',
            'child_ids': [(4, self.env.user.id)]
        })
        with self.assertRaises(Exception):
            reg.with_user(parent_user).write({'state': 'submitted'})
