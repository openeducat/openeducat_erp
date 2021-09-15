# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
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


class TestParent(TestParentCommon):

    def setUp(self):
        super(TestParent, self).setUp()

    def test_case_1_parent(self):
        parents = self.op_parent.search([])
        vals = {
            'name': self.env.ref('openeducat_core.op_res_partner_31').id,
            'user_id': self.env.ref('openeducat_parent.user_parent').id,
            'relationship_id': self.env.ref(
                'openeducat_parent.op_parent_relationship_1').id,
            'mobile': 8334845,
        }
        new_parent = self.op_parent.create(vals)
        new_parent.create_parent_user()
        student = self.env.ref('openeducat_parent.user_parent').id
        val = {'mobile': 77777777}
        self.op_parent.search([('user_id', '=', student)]).write(val)

        for parent in parents:
            parent._onchange_name()

        self.op_parent.search([('user_id', '=', student)]).unlink()

    def test_case_2_student(self):
        vals = {
            'user_id': self.env.ref('openeducat_parent.user_parent').id,
            'partner_id': self.env.ref('openeducat_parent.res_partner_33').id,
            'name': 'nikul',
            'last_name': 'ahir',
            'gender': 'm',
            'birth_date': '2009-01-01',
            'mobile': '73482383624',
            'email': 'nik@gmail.com',
            'parent_ids': [(6, 0, [self.env.ref('openeducat_parent.op_parent_1').id])],
        }

        self.op_student.create(vals)
        vals.update({
            'name': 'NIK AHiR',
            'parent_ids': [(6, 0, [self.env.ref('openeducat_parent.op_parent_1').id])],
        })
        self.op_student.write(vals)
        self.op_student.unlink()

    def test_case_3_subject_registartion(self):
        vals = {
            'student_id': self.env.ref('openeducat_core.op_student_1').id,
            'course_id': self.env.ref('openeducat_core.op_course_2').id,
            'batch_id': self.env.ref('openeducat_core.op_batch_1').id,
        }
        self.subject_registration.create(vals)
        self.subject_registration.write(vals)
