# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
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

from .test_core_common import TestCoreCommon


class TestCore(TestCoreCommon):

    def setUp(self):
        super(TestCore, self).setUp()

    def test_case_1_batch(self):
        batchs = self.op_batch.search([])

        for batch in batchs:
            batch.check_dates()
            batch.name_search('BOA-S1')

    def test_case_2_course(self):
        courses = self.op_course.search([])

        for course in courses:
            course.get_import_templates()

    def test_case_3_faculty(self):
        faculty = self.op_faculty.search([])

        new_faculty = self.op_faculty.create({
            'partner_id': self.env.ref('openeducat_core.op_res_partner_30').id,
            'first_name': 'binapshah',
            'last_name': 'kalol',
            'birth_date': '2009-01-01',
            'gender': 'male',
        })

        new_faculty._onchange_name()

        for rec in faculty:
            rec._check_birthdate()
            rec._onchange_name()
            rec.create_employee()
            rec.get_import_templates()

    def test_case_4_hr_employe(self):
        employs = self.hr_emp.search([])

        for employ in employs:
            employ.onchange_user()
            employ.onchange_address_id()

    def test_case_5_res_company(self):
        users = self.res_company.search([])
        record = self.env.ref('openeducat_core.op_faculty_1'),
        users.create_user(record)

    def test_case_6_student(self):
        students = self.op_student.search([])

        vals = {
            'first_name': 'nikul',
            'middle_name': 'm',
            'last_name': 'ahir',
            'birth_date': '1999-01-01',
            'gender': 'm',
            'partner_id': self.env.ref('openeducat_core.op_res_partner_14').id

        }
        new_student = self.op_student.create(vals)
        for student in students:
            student._onchange_name()
            student._check_birthdate()
            student.get_import_templates()
        new_student.create_student_user()

    def test_case_7_subject_registartion(self):
        vals = {
            'student_id': self.env.ref('openeducat_core.op_student_1').id,
            'course_id': self.env.ref('openeducat_core.op_course_2').id,
            'batch_id': self.env.ref('openeducat_core.op_batch_1').id,
        }
        registrations = self.subject_registration.create(vals)

        for registration in registrations:
            registration.action_reset_draft()
            registration.action_reject()
            registration.action_approve()
            registration.action_submitted()
            registration.get_subjects()

    def test_case_7_update(self):
        self.op_update._get_message()
        self.op_update.update_notification(cron_mode=True)

    def test_case_8_employ_wizard(self):

        vals = {'user_boolean': True}
        employe = self.employ_wizard.create(vals)
        employe.create_employee()

    def test_case_9_faculty_user_wizard(self):

        faculty_id = self.env.ref('openeducat_core.op_faculty_1')
        vals = {'faculty_ids': [(6, 0, [faculty_id.id])]}
        faculty = self.faculty_user_wizard.create(vals)
        faculty._get_faculties()
        faculty.create_faculty_user()

    def test_case_10_studnet_wizard(self):
        student_id = self.env.ref('openeducat_core.op_student_1')
        vals = {'student_ids': [(6, 0, [student_id.id])]}
        student = self.studnet_wizard.create(vals)
        student._get_students()
        student.create_user()
