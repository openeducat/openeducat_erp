"""Backfill ``op.session.student_ids`` for pre-existing sessions.

The ``student_ids`` M2M field was added to ``op.session`` in
19.0.1.1.0. Every session created before this upgrade has
``student_ids = []`` — which breaks the enterprise portal RPC
(``('student_ids', 'in', student.ids)`` returns nothing for those
sessions, making them invisible to students on the timetable page).

This script walks every session with an empty ``student_ids`` and
populates it from the same source the onchange handler uses:
``op.student.course`` entries matching the session's ``batch_id``.
Sessions with no batch are left alone (nothing to source from).

Safe to re-run; only touches rows where ``student_ids`` is still empty.
"""

import logging

from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    if not version:
        # Fresh install — no existing rows to backfill. Odoo passes
        # `version=None` for `-i`; only run on `-u` where a prior
        # module version was installed.
        return

    env = api.Environment(cr, SUPERUSER_ID, {})
    Session = env['op.session']
    Enrollment = env['op.student.course']

    # Sessions that have a batch but no allocated students. Skip
    # `active=False` too (archived sessions don't need touching for
    # the current portal use case; unarchive-then-re-save will
    # populate them if ever needed).
    sessions = Session.search([
        ('batch_id', '!=', False),
        ('student_ids', '=', False),
    ])
    if not sessions:
        _logger.info(
            "openeducat_timetable: student_ids backfill — nothing to do "
            "(no batch-scoped sessions with empty student_ids)."
        )
        return

    # Group sessions by batch so the enrollment lookup is one query
    # per batch instead of one per session.
    by_batch = {}
    for session in sessions:
        by_batch.setdefault(session.batch_id.id, env['op.session'])
        by_batch[session.batch_id.id] |= session

    all_batch_ids = list(by_batch.keys())
    # One query fetches every enrollment across every batch we need.
    enrollments = Enrollment.search([('batch_id', 'in', all_batch_ids)])
    students_by_batch = {}
    for enr in enrollments:
        students_by_batch.setdefault(
            enr.batch_id.id, env['op.student']
        )
        if enr.student_id:
            students_by_batch[enr.batch_id.id] |= enr.student_id

    total_pairs = 0
    total_sessions = 0
    for batch_id, batch_sessions in by_batch.items():
        student_ids = students_by_batch.get(batch_id)
        if not student_ids:
            continue
        # Single write per (batch, session set) — same students on
        # every session in that batch, so the write can be done in
        # one shot per session. Odoo will insert the M2M rows.
        # `no_calendar_sync=True` + `dont_notify=True` in case a
        # bridge module (Microsoft calendar, notify_user) has a
        # write-override on op.session — we don't want migration
        # to fire outbound emails or calendar syncs for old data.
        batch_sessions.with_context(
            no_calendar_sync=True, dont_notify=True,
        ).write({
            'student_ids': [(6, 0, student_ids.ids)],
        })
        total_pairs += len(batch_sessions) * len(student_ids)
        total_sessions += len(batch_sessions)

    _logger.info(
        "openeducat_timetable: student_ids backfill — populated %s sessions "
        "across %s batches (%s session/student pairs).",
        total_sessions, len(by_batch), total_pairs,
    )
