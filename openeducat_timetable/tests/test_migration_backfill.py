"""Cover the 19.0.1.1.0 post-migrate backfill.

Regression guards:
1. Sessions with batch_id but empty student_ids get populated.
2. Sessions with no batch_id are untouched.
3. Idempotent — running twice doesn't duplicate rows.
"""

from datetime import datetime
from importlib import util
from pathlib import Path

from odoo.tests import common


class TestMigrationBackfill(common.TransactionCase):

    def setUp(self):
        super().setUp()
        # Dynamically import the migration module — it lives outside
        # the Python addon path so a normal `import` won't find it.
        migration_path = Path(
            '/home/rohit/19.0/addons/openeducat_erp/'
            'openeducat_timetable/migrations/19.0.1.1.0/post-migrate.py'
        )
        spec = util.spec_from_file_location(
            'op_timetable_migration', migration_path,
        )
        self.migration_module = util.module_from_spec(spec)
        spec.loader.exec_module(self.migration_module)

        self.course = self.env.ref(
            'openeducat_core.op_course_2', raise_if_not_found=False)
        self.batch = self.env.ref(
            'openeducat_core.op_batch_1', raise_if_not_found=False)
        self.faculty = self.env.ref(
            'openeducat_core.op_faculty_1', raise_if_not_found=False)
        self.subject = self.env.ref(
            'openeducat_core.op_subject_1', raise_if_not_found=False)

    def _make_session(self, **overrides):
        vals = {
            'start_datetime': '2026-07-20 10:00:00',
            'end_datetime': '2026-07-20 11:00:00',
            'course_id': self.course.id,
            'faculty_id': self.faculty.id,
            'batch_id': self.batch.id,
            'subject_id': self.subject.id,
        }
        vals.update(overrides)
        return self.env['op.session'].create(vals)

    def test_backfill_populates_batch_sessions(self):
        if not self.batch:
            self.skipTest("No demo batch")
        enrolled = self.env['op.student.course'].search(
            [('batch_id', '=', self.batch.id)]).mapped('student_id')
        if not enrolled:
            self.skipTest("Demo batch has no enrolled students")
        # Regression guard: session with batch_id but empty
        # student_ids should end up populated.
        session = self._make_session()
        session.student_ids = [(5, 0, 0)]  # empty it
        self.assertFalse(session.student_ids)
        # Run migration with a non-None version → performs backfill.
        self.migration_module.migrate(self.env.cr, '19.0.1.0')
        session.invalidate_recordset(['student_ids'])
        # At least the enrolled students should now be attached.
        for stu in enrolled:
            self.assertIn(stu, session.student_ids)

    def test_backfill_skips_batchless_sessions(self):
        # Regression guard: sessions with no batch_id must NOT be
        # touched — nothing to source from.
        session = self._make_session()
        session.write({'batch_id': False})
        session.student_ids = [(5, 0, 0)]
        self.migration_module.migrate(self.env.cr, '19.0.1.0')
        session.invalidate_recordset(['student_ids'])
        self.assertFalse(session.student_ids)

    def test_backfill_idempotent(self):
        # Regression guard: running twice must not duplicate rows —
        # ON CONFLICT DO NOTHING (raw SQL variant) or Odoo's own
        # M2M semantics (`(6, 0, ids)` = replace) both handle this.
        if not self.batch:
            self.skipTest("No demo batch")
        session = self._make_session()
        self.migration_module.migrate(self.env.cr, '19.0.1.0')
        session.invalidate_recordset(['student_ids'])
        first_pass = set(session.student_ids.ids)
        self.migration_module.migrate(self.env.cr, '19.0.1.0')
        session.invalidate_recordset(['student_ids'])
        second_pass = set(session.student_ids.ids)
        self.assertEqual(first_pass, second_pass)

    def test_backfill_skipped_on_fresh_install(self):
        # Regression guard: `if not version: return` — Odoo passes
        # version=None on `-i`; skipping avoids running the query on
        # a brand-new DB.
        session = self._make_session()
        session.student_ids = [(5, 0, 0)]
        self.migration_module.migrate(self.env.cr, None)
        session.invalidate_recordset(['student_ids'])
        self.assertFalse(session.student_ids)
