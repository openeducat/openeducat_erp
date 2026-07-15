"""Shared fixtures for the new tests.

Kept separate from the existing ``test_timetable_common.py`` so we
don't disturb the pre-existing suite. Provides one small helper class
with course/batch/faculty/subject/students already wired up.
"""

from datetime import datetime, timedelta

from odoo import fields
from odoo.tests import common


class SessionFixtureCase(common.TransactionCase):
    """TransactionCase with a ready-made course + batch + faculty +
    subject + a few students, plus a `_make_session` helper.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Session = cls.env['op.session']
        cls.Course = cls.env['op.course']
        cls.Batch = cls.env['op.batch']
        cls.Faculty = cls.env['op.faculty']
        cls.Subject = cls.env['op.subject']
        cls.Student = cls.env['op.student']
        cls.Users = cls.env['res.users']
        cls.Partner = cls.env['res.partner']

        # Reuse the demo records shipped by openeducat_core so we
        # don't need to spin up a full course/batch graph from
        # scratch. Fall back to search() if refs go missing on some
        # customer installs.
        cls.course = cls._safe_ref(
            'openeducat_core.op_course_2') or cls.Course.search([], limit=1)
        cls.batch = cls._safe_ref(
            'openeducat_core.op_batch_1') or cls.Batch.search([], limit=1)
        cls.faculty = cls._safe_ref(
            'openeducat_core.op_faculty_1') or cls.Faculty.search([], limit=1)
        cls.subject = cls._safe_ref(
            'openeducat_core.op_subject_1') or cls.Subject.search([], limit=1)
        cls.students = cls.Student.search([], limit=3)

    @classmethod
    def _safe_ref(cls, xml_id):
        return cls.env.ref(xml_id, raise_if_not_found=False)

    def _make_session(self, start=None, end=None, **overrides):
        """Build a valid ``op.session`` dict + create it."""
        start = start or datetime(2026, 7, 20, 10, 0)
        end = end or datetime(2026, 7, 20, 11, 0)
        values = {
            'start_datetime': fields.Datetime.to_string(start),
            'end_datetime': fields.Datetime.to_string(end),
            'course_id': self.course.id,
            'faculty_id': self.faculty.id,
            'batch_id': self.batch.id,
            'subject_id': self.subject.id,
        }
        values.update(overrides)
        return self.Session.create(values)

    @staticmethod
    def _dt(y, m, d, hh=0, mm=0):
        return datetime(y, m, d, hh, mm)

    @staticmethod
    def _dt_shift(base, **kwargs):
        return base + timedelta(**kwargs)
