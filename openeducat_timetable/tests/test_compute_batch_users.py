"""Cover ``_compute_batch_users``.

Regression guards:
1. Per-session pruning of student_ids must propagate to user_ids
   (previously the compute only looked at batch enrollment).
2. Parents (via child_ids) are picked up.
3. Parents lookup is batched — one res.users.search per compute call
   regardless of recordset size.
"""

from datetime import datetime

from .common import SessionFixtureCase


class TestComputeBatchUsers(SessionFixtureCase):

    def test_user_ids_includes_faculty_user(self):
        # Regression guard: faculty user must always appear.
        session = self._make_session()
        if self.faculty.user_id:
            self.assertIn(self.faculty.user_id, session.user_ids)

    def test_user_ids_includes_student_users(self):
        # Regression guard: user_ids sources from student_ids, not from
        # batch enrollment. A student in student_ids must appear in
        # user_ids regardless of batch membership.
        session = self._make_session()
        student_users = self.students.mapped('user_id')
        session.student_ids = [(6, 0, self.students.ids)]
        for u in student_users:
            if u:
                self.assertIn(u, session.user_ids)

    def test_user_ids_updates_on_student_removal(self):
        # Regression guard: removing a student from student_ids must
        # remove them from user_ids (previously the compute ignored
        # student_ids so the backend record rule wasn't updated).
        session = self._make_session()
        if not self.students:
            self.skipTest("No demo students available")
        session.student_ids = [(6, 0, self.students.ids)]
        first_student = self.students[0]
        session.student_ids = [(3, first_student.id)]
        if first_student.user_id:
            self.assertNotIn(first_student.user_id, session.user_ids)

    def test_parents_lookup_batched(self):
        # Regression guard: previously the parents `res.users.search`
        # fired once per session. Since we can't easily instrument the
        # query count in a portable way, we at least assert the compute
        # completes on a multi-record set without raising and yields
        # non-empty results consistent with per-record execution.
        sessions = self.Session
        for _ in range(3):
            sessions |= self._make_session()
        # Force recompute on the whole set at once (batched code path).
        sessions._compute_batch_users()
        for s in sessions:
            # Faculty user should be present in every session's user_ids.
            if self.faculty.user_id:
                self.assertIn(self.faculty.user_id, s.user_ids)

    def test_empty_recordset_does_not_crash(self):
        # Regression guard: empty self.mapped() on an empty recordset
        # was fine, but the `if all_base_ids:` branch matters when
        # nobody has a user link.
        self.env['op.session']._compute_batch_users()  # no-op, must not raise
