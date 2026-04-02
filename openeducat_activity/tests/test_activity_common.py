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

from odoo.tests import TransactionCase


class TestActivityCommon(TransactionCase):
    def setUp(self):
        super(TestActivityCommon, self).setUp()
        self.op_activity_type = self.env['op.activity.type']
        self.op_activity = self.env['op.activity']
        self.op_student_migrate_wizard = self.env['student.migrate']

        # Setup basic data for tests
        self.course_1 = self.env['op.course'].create({
            'name': 'Course 1',
            'code': 'C1'
        })
        self.course_2 = self.env['op.course'].create({
            'name': 'Course 2',
            'code': 'C2',
            'parent_id': self.course_1.id
        })
        self.course_3 = self.env['op.course'].create({
            'name': 'Course 3',
            'code': 'C3',
            'parent_id': self.course_1.id
        })
        self.batch_1 = self.env['op.batch'].create({
            'name': 'Batch 1',
            'code': 'B1',
            'course_id': self.course_1.id,
            'start_date': '2025-01-01',
            'end_date': '2025-12-31'
        })
        self.batch_2 = self.env['op.batch'].create({
            'name': 'Batch 2',
            'code': 'B2',
            'course_id': self.course_2.id,
            'start_date': '2025-01-01',
            'end_date': '2025-12-31'
        })
        
        self.faculty_user = self.env['res.users'].create({
            'name': 'Test Faculty User',
            'login': 'faculty_test',
            'email': 'faculty@test.com',
            'group_ids': [(6, 0, [
                self.env.ref('base.group_user').id,
                self.env.ref('openeducat_core.group_op_faculty').id,
                self.env.ref('openeducat_activity.group_activity_manager').id
            ])]
        })
        self.faculty = self.env['op.faculty'].create({
            'first_name': 'Test',
            'last_name': 'Faculty',
            'gender': 'male',
            'birth_date': '1990-01-01',
            'user_id': self.faculty_user.id
        })
        
        self.student = self.env['op.student'].create({
            'first_name': 'Test',
            'last_name': 'Student',
            'gender': 'm',
            'birth_date': '2000-01-01'
        })
        
        # Enroll student in course_2
        self.env['op.student.course'].create({
            'student_id': self.student.id,
            'course_id': self.course_2.id,
            'batch_id': self.batch_2.id,
            'state': 'running'
        })
        
        # Ensure Academic Migration activity type exists with XML ID for wizard tests
        existing_type_ref = self.env.ref('openeducat_activity.op_activity_type_3', raise_if_not_found=False)
        if not existing_type_ref:
            self.type_migration = self.op_activity_type.create({
                'name': 'Academic Migration'
            })
            self.env['ir.model.data'].create({
                'name': 'op_activity_type_3',
                'module': 'openeducat_activity',
                'model': 'op.activity.type',
                'res_id': self.type_migration.id,
            })
        else:
            self.type_migration = existing_type_ref
