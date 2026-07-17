"""Cover ``_sync_session_followers`` on create() + write().

Regression guards:
1. create() subscribes faculty user's partner + student users' partners.
2. write() diff unsubscribes partners newly removed from student_ids.
3. Manual followers (added via chatter Follow) are LEFT ALONE.
"""

from datetime import datetime

from .common import SessionFixtureCase


class TestFollowerSync(SessionFixtureCase):

    def test_create_subscribes_faculty_and_students(self):
        session = self._make_session()
        if self.students:
            session.student_ids = [(6, 0, self.students.ids)]
            # Force a re-sync (write path).
            session._sync_session_followers()
        current = session.message_follower_ids.mapped('partner_id')
        expected = session._session_follower_partners()
        for partner in expected:
            self.assertIn(partner, current)

    def test_write_unsubscribes_removed_students(self):
        # Regression guard: removing a student from student_ids must
        # unsubscribe them (previously the write() didn't diff).
        if not self.students or len(self.students) < 2:
            self.skipTest("Need at least 2 demo students")
        session = self._make_session(student_ids=[(6, 0, self.students.ids)])
        target = self.students[0]
        target_user = target.user_id
        if not target_user:
            self.skipTest("First student has no linked user")
        target_partner = target_user.partner_id
        # Sanity: they ARE currently a follower.
        self.assertIn(
            target_partner, session.message_follower_ids.mapped('partner_id'),
        )
        # Remove them.
        session.write({'student_ids': [(3, target.id)]})
        # They should no longer be a follower.
        self.assertNotIn(
            target_partner, session.message_follower_ids.mapped('partner_id'),
        )

    def test_manual_follower_preserved(self):
        # Regression guard: only partners in `old_desired` may be
        # unsubscribed. A manually-added follower must survive a
        # student_ids write cycle.
        session = self._make_session()
        # Pick an unrelated partner (admin's partner should exist).
        manual = self.env.ref('base.partner_root', raise_if_not_found=False)
        if not manual:
            self.skipTest("base.partner_root missing")
        session.message_subscribe(partner_ids=[manual.id])
        session.write({'student_ids': [(6, 0, [])]})  # clear
        current = session.message_follower_ids.mapped('partner_id')
        self.assertIn(manual, current)
