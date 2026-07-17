"""Cover ``_onchange_batch_id_populate_students``.

Regression guards:
1. Picking a batch pre-fills student_ids from op.student.course.
2. Clearing batch_id clears student_ids.
"""

from datetime import datetime

from odoo.tests.common import Form

from .common import SessionFixtureCase


class TestOnchangeBatchPopulate(SessionFixtureCase):

    def test_batch_populates_students(self):
        # Regression guard: enrollment lookup uses op.student.course
        # (not batch.student_ids — that field may not exist).
        if not self.batch:
            self.skipTest("No demo batch")
        # Ensure at least one enrollment on the batch we're testing.
        enrollment_count = self.env['op.student.course'].search_count(
            [('batch_id', '=', self.batch.id)])
        if enrollment_count == 0:
            self.skipTest("Demo batch has no enrolled students")
        with Form(self.Session) as form:
            form.start_datetime = datetime(2026, 7, 20, 10, 0)
            form.end_datetime = datetime(2026, 7, 20, 11, 0)
            form.course_id = self.course
            form.faculty_id = self.faculty
            form.subject_id = self.subject
            form.batch_id = self.batch
            # After onchange, student_ids should be populated.
            self.assertTrue(
                form.student_ids,
                "Batch onchange should populate student_ids from enrollments",
            )

    def test_clearing_batch_clears_students(self):
        # Regression guard: onchange with batch_id=False sets
        # student_ids to [(5, 0, 0)] (clear).
        session = self._make_session()
        if not self.students:
            self.skipTest("No demo students")
        session.student_ids = [(6, 0, self.students.ids)]
        self.assertTrue(session.student_ids)
        # Now simulate the onchange by unsetting batch and re-running.
        with Form(session) as form:
            form.batch_id = self.env['op.batch']
            # After onchange, student_ids should be empty.
            self.assertFalse(
                form.student_ids,
                "Clearing batch should clear student_ids",
            )
