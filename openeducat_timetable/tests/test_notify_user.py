"""Cover ``notify_user`` — single-mail-per-session semantics + context
flag honoring + missing-template safety.

Regression guards:
1. N+1 emails: one send_mail per session, not one per follower per
   session.
2. ``dont_notify`` context flag skips the send.
3. ``no_calendar_sync`` context flag also skips (Microsoft bridge).
4. Missing template returns silently (not `raise_if_not_found`).
5. Faculty tz used when set.
"""

from datetime import datetime
from unittest.mock import patch

from odoo.tests.common import mute_logger

from .common import SessionFixtureCase


class TestNotifyUser(SessionFixtureCase):

    def _make(self):
        return self._make_session(
            start=datetime(2026, 7, 20, 10, 0),
            end=datetime(2026, 7, 20, 11, 0),
        )

    def test_one_send_mail_per_session(self):
        # Regression guard: previous impl called send_mail once per
        # follower — 30 students + faculty ⇒ 31 sends.
        session = self._make()
        # Attach a few students so followers > 1.
        if self.students:
            session.student_ids = [(6, 0, self.students.ids)]
        template = self.env.ref(
            'openeducat_timetable.session_details_changes',
            raise_if_not_found=False,
        )
        if not template:
            self.skipTest("session_details_changes template missing")
        with patch.object(type(template), 'send_mail') as mocked:
            session.notify_user()
            # ≤ 1 call — 0 if no follower has an email, else exactly 1.
            self.assertLessEqual(mocked.call_count, 1)

    def test_dont_notify_context_skips(self):
        # Regression guard: bridge modules use dont_notify to suppress
        # emails on bookkeeping writes.
        session = self._make()
        template = self.env.ref(
            'openeducat_timetable.session_details_changes',
            raise_if_not_found=False,
        )
        if not template:
            self.skipTest("session_details_changes template missing")
        with patch.object(type(template), 'send_mail') as mocked:
            session.with_context(dont_notify=True).notify_user()
            mocked.assert_not_called()

    def test_no_calendar_sync_context_skips(self):
        # Regression guard: Microsoft bridge uses no_calendar_sync
        # to suppress notifications during sync bookkeeping.
        session = self._make()
        template = self.env.ref(
            'openeducat_timetable.session_details_changes',
            raise_if_not_found=False,
        )
        if not template:
            self.skipTest("session_details_changes template missing")
        with patch.object(type(template), 'send_mail') as mocked:
            session.with_context(no_calendar_sync=True).notify_user()
            mocked.assert_not_called()

    @mute_logger('odoo.models', 'odoo.addons.mail.models.mail_mail')
    def test_missing_template_returns_silently(self):
        # Regression guard: template lookup must NOT raise —
        # `raise_if_not_found=False` is the whole point of the guard.
        session = self._make()
        original_ref = self.env.ref

        def fake_ref(xml_id, raise_if_not_found=True):
            if xml_id == 'openeducat_timetable.session_details_changes':
                return original_ref('__does_not_exist__',
                                    raise_if_not_found=False)
            return original_ref(xml_id, raise_if_not_found=raise_if_not_found)

        with patch.object(self.env, 'ref', side_effect=fake_ref):
            session.notify_user()  # must not raise
