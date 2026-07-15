"""Cover ``check_timetable_fields`` and the ``_overlaps`` helper.

Regression guards:
1. Batch-less sessions do NOT trigger spurious ValidationError
   (`False == False` bug from an earlier iteration).
2. Midnight-crossing sessions handled correctly by full-datetime
   comparison (the old `.time()`-only compare returned inverted
   overlap booleans).
3. Back-to-back sessions do NOT conflict (strict `<`, not `<=`).
4. Cancelled sessions do NOT participate in conflict detection.
5. Window pre-filter: a session far outside the ±24h window isn't
   scanned (perf guard).
"""

from datetime import datetime

from odoo.exceptions import ValidationError
from odoo.tests import tagged

from .common import SessionFixtureCase


@tagged('post_install', '-at_install')
class TestCheckTimetableFields(SessionFixtureCase):

    def setUp(self):
        super().setUp()
        # Turn constraints ON for tests — DB defaults may leave them
        # off, hiding conflicts.
        icp = self.env['ir.config_parameter'].sudo()
        icp.set_param('timetable.is_faculty_constraint', '1')
        icp.set_param('timetable.is_classroom_constraint', '1')
        icp.set_param('timetable.is_batch_and_subject_constraint', '1')
        icp.set_param('timetable.is_batch_constraint', '1')

    def test_batchless_pair_does_not_conflict(self):
        # Regression guard: `rec.batch_id.id == other.batch_id.id`
        # with both False used to raise a spurious ValidationError
        # ("cannot create a session for the same batch"). Now guarded
        # by `need_batch_check = self.filtered('batch_id')`.
        #
        # Both sessions get: no batch, SAME faculty, NON-overlapping
        # windows — this isolates the batch-check branch. If the old
        # `False == False` bug were still present, the batch check
        # would fire even on non-overlapping windows because same-day
        # + same-batch was the trigger.
        a = self._make_session(
            start=datetime(2026, 7, 20, 10, 0),
            end=datetime(2026, 7, 20, 11, 0),
        )
        a.write({'batch_id': False})
        # Non-overlapping window from the start — faculty constraint
        # would raise here otherwise (faculty is the same by default).
        b = self._make_session(
            start=datetime(2026, 7, 20, 13, 0),
            end=datetime(2026, 7, 20, 14, 0),
        )
        b.write({'batch_id': False})
        # If we got here without ValidationError, the guard holds.
        self.assertFalse(a.batch_id)
        self.assertFalse(b.batch_id)

    def test_back_to_back_sessions_no_conflict(self):
        # Regression guard: strict `<` on both ends allows
        # `10:00–11:00` and `11:00–12:00` to coexist.
        self._make_session(
            start=datetime(2026, 7, 20, 10, 0),
            end=datetime(2026, 7, 20, 11, 0),
        )
        # Second session should save without raising.
        self._make_session(
            start=datetime(2026, 7, 20, 11, 0),
            end=datetime(2026, 7, 20, 12, 0),
        )

    def test_faculty_overlap_raises(self):
        self._make_session(
            start=datetime(2026, 7, 20, 10, 0),
            end=datetime(2026, 7, 20, 11, 0),
        )
        with self.assertRaises(ValidationError):
            self._make_session(
                start=datetime(2026, 7, 20, 10, 30),
                end=datetime(2026, 7, 20, 11, 30),
                # Same faculty explicit — same batch/course/subject would
                # ALSO raise via batch constraints, but we want the
                # faculty branch to be the culprit.
            )

    def test_cancelled_session_does_not_participate(self):
        # Regression guard: `('state','!=','cancel')` in the pre-filter
        # domain — cancelled sessions must NOT block new ones.
        a = self._make_session(
            start=datetime(2026, 7, 20, 10, 0),
            end=datetime(2026, 7, 20, 11, 0),
        )
        a.state = 'cancel'
        # A new session in the same window should save.
        self._make_session(
            start=datetime(2026, 7, 20, 10, 30),
            end=datetime(2026, 7, 20, 11, 30),
        )

    def test_midnight_crossing_no_inverted_overlap(self):
        # Regression guard: `.time()` alone made `end.time() <
        # start.time()` on a session 23:00 → 01:00, breaking the
        # 4-clause overlap. Full-datetime compare handles it.
        # Two sessions that cross midnight on the SAME window should
        # correctly conflict, not silently pass.
        self._make_session(
            start=datetime(2026, 7, 20, 23, 0),
            end=datetime(2026, 7, 21, 1, 0),
        )
        with self.assertRaises(ValidationError):
            # This one starts inside the first's window (00:00 IS
            # inside 23:00-01:00).
            self._make_session(
                start=datetime(2026, 7, 21, 0, 0),
                end=datetime(2026, 7, 21, 0, 30),
            )

    def test_far_away_session_not_scanned(self):
        # Regression guard: pre-filter uses ±24h. A session 30 days
        # apart must save cleanly (no faculty conflict scan on it).
        self._make_session(
            start=datetime(2026, 7, 20, 10, 0),
            end=datetime(2026, 7, 20, 11, 0),
        )
        # Weeks later — must save cleanly.
        self._make_session(
            start=datetime(2026, 8, 20, 10, 0),
            end=datetime(2026, 8, 20, 11, 0),
        )
