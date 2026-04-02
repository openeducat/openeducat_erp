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

from odoo.tests import common


class TestParentCommon(common.TransactionCase):
    def setUp(self):
        super(TestParentCommon, self).setUp()
        self.op_parent = self.env['op.parent']
        self.op_student = self.env['op.student']
        self.subject_registration = self.env['op.subject.registration']
        self.op_parent_relationship = self.env['op.parent.relationship']

        # Setup base data
        self.course = self.env['op.course'].create({'name': 'Test Course', 'code': 'TC1'})
        self.batch = self.env['op.batch'].create({
            'name': 'Test Batch', 'code': 'TB1', 'course_id': self.course.id,
            'start_date': '2025-01-01', 'end_date': '2025-12-31'
        })
        self.student_partner = self.env['res.partner'].create({'name': 'Test Student'})
        self.student = self.env['op.student'].create({
            'partner_id': self.student_partner.id,
            'first_name': 'Test',
            'last_name': 'Student',
            'gender': 'm',
            'birth_date': '2010-01-01',
        })
        self.parent_partner = self.env['res.partner'].create({
            'name': 'Robust Parent',
            'email': 'robust_parent@example.com',
            'phone': '1234567890',
            'is_parent': True
        })
        self.rel_father = self.env['op.parent.relationship'].search([('name', '=', 'Test Father')], limit=1)
        if not self.rel_father:
            self.rel_father = self.env['op.parent.relationship'].create({'name': 'Test Father'})
        
        self.rel_mother = self.env['op.parent.relationship'].search([('name', '=', 'Test Mother')], limit=1)
        if not self.rel_mother:
            self.rel_mother = self.env['op.parent.relationship'].create({'name': 'Test Mother'})
