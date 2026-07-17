"""Cover the ``act_gen_time_table`` wizard.

Regression guard: wizard bulk-creates sessions via
``session_obj.create(data)``. This bypasses the
``_onchange_batch_id_populate_students`` onchange. Without the fix,
generated sessions had empty student_ids and were invisible on the
enterprise portal. Fix pre-computes enrollment ids and attaches them
via ``[(6, 0, ...)]`` on every session dict.
"""

import time
from datetime import date

from odoo import fields
from odoo.tests import common


class TestWizardStudentIds(common.TransactionCase):

    def setUp(self):
        super().setUp()
        self.course = self.env.ref(
            'openeducat_core.op_course_2', raise_if_not_found=False)
        self.batch = self.env.ref(
            'openeducat_core.op_batch_1', raise_if_not_found=False)
        self.faculty = self.env.ref(
            'openeducat_core.op_faculty_1', raise_if_not_found=False)
        self.subject = self.env.ref(
            'openeducat_core.op_subject_1', raise_if_not_found=False)
        self.timing = self.env.ref(
            'openeducat_timetable.op_timing_1', raise_if_not_found=False)

    def test_generated_sessions_have_student_ids(self):
        if not (self.course and self.batch and self.faculty
                and self.subject):
            self.skipTest("Missing demo records")
        enrolled = self.env['op.student.course'].search(
            [('batch_id', '=', self.batch.id)])
        if not enrolled:
            self.skipTest("No enrollments on demo batch — nothing to backfill")
        expected_students = enrolled.mapped('student_id')

        # Same weekday all year — pick tomorrow so day-of-week matches.
        target = date(2026, 7, 20)  # Monday
        wizard = self.env['generate.time.table'].create({
            'course_id': self.course.id,
            'batch_id': self.batch.id,
            'start_date': target,
            'end_date': target,
        })
        self.env['gen.time.table.line'].create({
            'gen_time_table': wizard.id,
            'faculty_id': self.faculty.id,
            'subject_id': self.subject.id,
            'session_start_time': 10.0,
            'session_end_time': 11.0,
            'day': str(target.weekday()),
        })
        # Snapshot existing sessions so we can find the new one.
        existing = self.env['op.session'].search([])
        wizard.act_gen_time_table()
        new_sessions = self.env['op.session'].search([]) - existing
        self.assertTrue(new_sessions, "Wizard should create at least one session")
        for s in new_sessions:
            for stu in expected_students:
                self.assertIn(
                    stu, s.student_ids,
                    "Wizard-created session should carry the batch's student_ids",
                )
