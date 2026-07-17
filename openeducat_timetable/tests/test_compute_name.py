"""Cover ``_compute_name`` — same tz surface as ``_compute_timing``.

Regression guards: the old `pytz.timezone(user.tz).astimezone(dt)`
pattern was doubly wrong (crashed on None tz, misconverted naive
UTC). Format expected: ``Faculty:Subject:HH:MMxx-HH:MMxx``.
"""

from datetime import datetime

from .common import SessionFixtureCase


class TestComputeName(SessionFixtureCase):

    def _make(self, tz):
        self.env.user.tz = tz
        return self._make_session(
            start=datetime(2026, 7, 20, 10, 0),
            end=datetime(2026, 7, 20, 11, 0),
        )

    def test_name_utc(self):
        session = self._make('UTC')
        session._compute_name()
        expected = '%s:%s:10:00AM-11:00AM' % (
            self.faculty.name, self.subject.name,
        )
        self.assertEqual(session.name, expected)

    def test_name_ist(self):
        session = self._make('Asia/Kolkata')
        session._compute_name()
        expected = '%s:%s:03:30PM-04:30PM' % (
            self.faculty.name, self.subject.name,
        )
        self.assertEqual(session.name, expected)

    def test_name_none_tz_does_not_crash(self):
        # Regression guard: pytz.timezone(None) raised UnknownTimeZoneError.
        session = self._make(False)
        session._compute_name()
        self.assertIn(self.faculty.name, session.name or '')
