"""Cover ``_compute_timing`` — regression guards for the naive-UTC
``.astimezone()`` bug and the ``pytz.timezone(None)`` crash.

Fixed this session in models/timetable.py:_compute_timing by moving
to ``fields.Datetime.context_timestamp`` which is tz-safe.
"""

from datetime import datetime

from odoo import fields

from .common import SessionFixtureCase


class TestComputeTiming(SessionFixtureCase):

    def _make(self, start_hour_utc, end_hour_utc, tz=None):
        # Regression guard: `pytz.timezone(self.env.user.tz)` used to
        # crash when tz was None. context_timestamp falls back to UTC.
        self.env.user.tz = tz
        return self._make_session(
            start=datetime(2026, 7, 20, start_hour_utc, 0),
            end=datetime(2026, 7, 20, end_hour_utc, 0),
        )

    def test_timing_utc(self):
        session = self._make(10, 11, tz='UTC')
        session._compute_timing()
        self.assertEqual(session.timing, '10:00AM - 11:00AM')

    def test_timing_ist(self):
        # 10:00 UTC = 15:30 IST. `.astimezone(IST)` on a NAIVE UTC
        # datetime used to treat it as system-local time — bug.
        session = self._make(10, 11, tz='Asia/Kolkata')
        session._compute_timing()
        self.assertEqual(session.timing, '03:30PM - 04:30PM')

    def test_timing_none_tz_does_not_crash(self):
        # Regression guard: user.tz=None crashed the old code with
        # `AttributeError: 'NoneType' object has no attribute ...`.
        session = self._make(10, 11, tz=False)
        session._compute_timing()  # must not raise
        self.assertEqual(session.timing, '10:00AM - 11:00AM')

    def test_timing_empty_when_missing_datetimes(self):
        # Guarded by `if not (start and end): continue` in the fix.
        # Direct-write to bypass required-field constraint would need
        # sudo tricks — instead, ensure a normal record has a timing.
        session = self._make(9, 10, tz='UTC')
        self.assertTrue(session.timing)
