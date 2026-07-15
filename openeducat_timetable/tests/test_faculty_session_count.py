"""Cover ``op.faculty._compute_session_details``.

Regression guard: the pre-fix code did
``self.env['op.session'].search_count([('faculty_id','=',self.id)])``
where ``self`` was the whole recordset — every faculty ended up with
the count for the first faculty's id (or a singleton-error crash on
multi-record recompute). Fix replaces with `len(faculty.session_ids)`.
"""

from datetime import datetime

from .common import SessionFixtureCase


class TestFacultySessionCount(SessionFixtureCase):

    def test_count_per_faculty_correct(self):
        # Create three sessions for the same faculty across a small
        # date window, then assert the counter matches.
        for offset in range(3):
            self._make_session(
                start=datetime(2026, 7, 20 + offset, 10, 0),
                end=datetime(2026, 7, 20 + offset, 11, 0),
            )
        self.faculty.invalidate_recordset(['session_count'])
        self.assertEqual(self.faculty.session_count, len(self.faculty.session_ids))
        self.assertGreaterEqual(self.faculty.session_count, 3)

    def test_multi_faculty_recompute_no_singleton_error(self):
        # Regression guard: the old code crashed with
        # `singleton expected` on a multi-record recompute because
        # `self.id` inside `for session in self` blows up on len > 1.
        many = self.Faculty.search([], limit=5)
        # Just triggering the compute on a multi-record set must NOT
        # raise; the values themselves are validated elsewhere.
        many._compute_session_details()
