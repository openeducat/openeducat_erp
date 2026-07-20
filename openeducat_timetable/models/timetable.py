###############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<https://www.openeducat.org>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class OpSession(models.Model):
    _name = "op.session"
    _inherit = ["mail.thread"]
    _description = "Sessions"

    name = fields.Char(compute='_compute_name', string='Name', store=True)
    timing_id = fields.Many2one(
        'op.timing', 'Timing', tracking=True)
    start_datetime = fields.Datetime(
        'Start Time', required=True, index=True, tracking=True,
        default=lambda self: fields.Datetime.now())
    end_datetime = fields.Datetime(
        'End Time', required=True, tracking=True)
    course_id = fields.Many2one(
        'op.course', 'Course', required=True, tracking=True)
    faculty_id = fields.Many2one(
        'op.faculty', 'Faculty', required=True, tracking=True,
        default=lambda self: self._default_faculty_id())
    batch_id = fields.Many2one(
        'op.batch', 'Batch', required=True, tracking=True)
    subject_id = fields.Many2one(
        'op.subject', 'Subject', required=True, tracking=True)
    classroom_id = fields.Many2one(
        'op.classroom', 'Classroom', tracking=True)
    color = fields.Integer('Color Index')
    type = fields.Char(compute='_compute_day', string='Day', store=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirmed'),
         ('done', 'Done'), ('cancel', 'Canceled')],
        string='Status', default='draft', tracking=True)
    user_ids = fields.Many2many(
        'res.users', compute='_compute_batch_users',
        store=True, string='Users')
    student_ids = fields.Many2many(
        'op.student', string='Students',
        help='Students attending this session. Auto-populated from the '
             'batch when Batch is picked; you can remove individuals '
             'afterwards if the session isn\'t for the whole cohort.',
    )
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.user.company_id)
    days = fields.Selection([
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday')],
        'Days',
        group_expand='_expand_groups', store=True
    )
    timing = fields.Char(compute='_compute_timing', string='Session timing')
    # Helper for the calendar quick-create view: exposes the chosen
    # course's subject list so we can filter `subject_id` with a
    # simple `domain="[('id', 'in', course_subject_ids)]"` — avoids
    # cross-record dotted-path lookups that view domains can't evaluate.
    course_subject_ids = fields.Many2many(
        'op.subject',
        related='course_id.subject_ids',
        string='Course Subjects',
        readonly=True,
    )

    @api.model
    def _default_faculty_id(self):
        """Pre-fill `faculty_id` with the faculty record linked to
        the currently logged-in user.

        Match via `partner_id` (not `emp_id.user_id`) — every op.faculty
        has a `partner_id` because it's the `_inherits` key on
        res.partner, but `emp_id` (hr.employee link) is optional and
        often unset when faculty rows were created outside the
        "employee onboarding" flow. Matching on partner works for
        every faculty that maps to a user, which is the intended
        universe.

        Fall back to False when the current user isn't a faculty —
        picker stays empty and the user picks manually.
        """
        if not self.env.user.partner_id:
            return False
        faculty = self.env["op.faculty"].sudo().search(
            [("partner_id", "=", self.env.user.partner_id.id)], limit=1,
        )
        return faculty.id if faculty else False

    @api.depends('start_datetime', 'end_datetime')
    def _compute_timing(self):
        for session in self:
            if not (session.start_datetime and session.end_datetime):
                continue
            # Odoo stores datetimes as naive UTC. context_timestamp
            # localizes as UTC then converts to the record's env tz —
            # also safe when user.tz is None (falls back to UTC),
            # unlike `pytz.timezone(self.env.user.tz)` which crashes.
            start = fields.Datetime.context_timestamp(session, session.start_datetime)
            end = fields.Datetime.context_timestamp(session, session.end_datetime)
            session.timing = (
                start.strftime('%I:%M%p') + ' - ' + end.strftime('%I:%M%p')
            )

    @api.model
    def _expand_groups(self, days, domain, order=None):
        weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
                    'sunday']
        return [day for day in weekdays if day in days]

    @api.depends('start_datetime')
    def _compute_day(self):
        days = {0: 'monday', 1: 'tuesday', 2: 'wednesday', 3: 'thursday', 4: 'friday',
                5: 'saturday', 6: 'sunday'}
        for record in self:
            if record.start_datetime:
                record.type = days.get(record.start_datetime.weekday()).capitalize()
                record.days = days.get(record.start_datetime.weekday())

    @api.depends('faculty_id', 'subject_id', 'start_datetime', 'end_datetime')
    def _compute_name(self):
        for session in self:
            if not (session.faculty_id and session.subject_id
                    and session.start_datetime and session.end_datetime):
                continue
            # Same tz-safe conversion as _compute_timing above.
            start = fields.Datetime.context_timestamp(session, session.start_datetime)
            end = fields.Datetime.context_timestamp(session, session.end_datetime)
            session.name = (
                session.faculty_id.name + ':' +
                session.subject_id.name + ':' +
                start.strftime('%I:%M%p') + '-' +
                end.strftime('%I:%M%p')
            )

    # For record rule on student and faculty dashboard.
    # Sources users directly from `student_ids` + `faculty_id.user_id`
    # instead of searching by batch — respects per-session pruning
    # (the backend `student_session_rule` gates on `user_ids`, so
    # removing a student from `student_ids` now propagates to backend
    # visibility, not just the portal).
    @api.depends('student_ids.user_id', 'faculty_id.user_id')
    def _compute_batch_users(self):
        # Batched parents lookup: collect the union of every session's
        # base users first, run ONE `res.users.search` for parents
        # across the whole set, then intersect back per session.
        # Previously the parents search fired per record → N+1 that
        # showed up on wizard-generated recomputes.
        base_by_session = {}
        all_base_ids = set()
        for session in self:
            base = (
                session.student_ids.mapped('user_id')
                | session.faculty_id.user_id
            )
            base_by_session[session.id] = base
            all_base_ids.update(base.ids)

        if all_base_ids:
            all_parents = self.env['res.users'].search(
                [('child_ids', 'in', list(all_base_ids))],
            )
            # Reverse index: base_user_id → parents-of-that-user
            parents_of = {}
            for parent in all_parents:
                for child in parent.child_ids:
                    parents_of.setdefault(child.id, self.env['res.users'])
                    parents_of[child.id] |= parent
        else:
            parents_of = {}

        for session in self:
            base = base_by_session[session.id]
            parents = self.env['res.users']
            for child_id in base.ids:
                parents |= parents_of.get(child_id, self.env['res.users'])
            session.user_ids = base | parents

    @api.onchange('batch_id')
    def _onchange_batch_id_populate_students(self):
        """Auto-populate `student_ids` with every student enrolled in
        the chosen batch. Same UX as `op.assignment.allocation_ids`
        — the editor sees the full roster pre-filled and can prune
        individuals if a session doesn't apply to everyone.

        Walks `op.student.course` (the enrollment link table) so
        students who transferred out of the batch don't leak in from
        old enrollments.
        """
        if not self.batch_id:
            self.student_ids = [(5, 0, 0)]
            return
        enrollments = self.env['op.student.course'].search(
            [('batch_id', '=', self.batch_id.id)]
        )
        self.student_ids = [(6, 0, enrollments.mapped('student_id').ids)]

    def lecture_draft(self):
        self.state = 'draft'

    def lecture_confirm(self):
        self.state = 'confirm'

    def lecture_done(self):
        self.state = 'done'

    def lecture_cancel(self):
        self.state = 'cancel'

    @api.constrains('start_datetime', 'end_datetime')
    def _check_date_time(self):
        for rec in self:
            if rec.start_datetime > rec.end_datetime:
                raise ValidationError(_(
                    'End Time cannot be set before Start Time.'))

    @api.constrains('faculty_id', 'start_datetime', 'end_datetime', 'classroom_id',
                    'batch_id', 'subject_id')
    def check_timetable_fields(self):
        res_param = self.env['ir.config_parameter'].sudo()
        is_faculty_constraint = res_param.search([
            ('key', '=', 'timetable.is_faculty_constraint')]).value
        is_classroom_constraint = res_param.search([
            ('key', '=', 'timetable.is_classroom_constraint')]).value
        is_batch_and_subject_constraint = res_param.search([
            ('key', '=', 'timetable.is_batch_and_subject_constraint')]).value
        is_batch_constraint = res_param.search([
            ('key', '=', 'timetable.is_batch_constraint')]).value

        # Batch- and batch-and-subject constraints compare `batch_id.id`
        # equality. Two sessions with no batch would compare
        # `False == False` → spurious ValidationError. Enterprise
        # relaxes batch_id to `required=False` (ad-hoc scheduling),
        # so we drop batch-less records from batch-related checks.
        # Faculty and classroom checks stay on every record.
        need_batch_check = self.filtered('batch_id')

        # Pre-filter the "other sessions" search by a date window
        # covering the range being saved. Previously `search([])` did
        # a full-table scan then O(N·M) nested loop — 10k-session DB
        # meant every save iterated 10k×len(self) records. Since
        # conflicts only exist same-day, ±24h is generous headroom
        # for tz edge cases and multi-day sessions.
        if not self:
            return
        dt_min = min(self.mapped('start_datetime')) - timedelta(hours=24)
        dt_max = max(self.mapped('end_datetime')) + timedelta(hours=24)
        other_domain = [
            ('id', 'not in', self.ids),
            ('state', '!=', 'cancel'),           # cancelled sessions don't conflict
            ('start_datetime', '>=', dt_min),
            ('start_datetime', '<=', dt_max),
        ]
        # sudo(): the conflict search MUST see every session in the
        # window, not just what the current user's record rules
        # expose. A faculty user creating a session doesn't have
        # read on OTHER faculties' sessions (student_session_rule /
        # user_session_rule gate on `user_ids`), so without sudo
        # the constraint silently passes on cross-faculty overlaps
        # — exactly the "sessions 8 and 9" bug. Only fact of
        # existence + a name is surfaced in the error message,
        # nothing sensitive.
        others = self.env['op.session'].sudo().search(other_domain)

        def _overlaps(a, b):
            """Full-datetime window overlap.

            Compares the raw naive-UTC datetimes directly. Handles:
              * Sessions spanning midnight (23:00 → 01:00) — the
                previous `.time()`-only compare returned inverted
                booleans because `end.time() < start.time()`.
              * Sessions near a tz boundary (23:00 UTC = 04:00 IST
                next day) — the previous `.date()` split bucketed
                them differently and missed same-local-day conflicts.

            Strict `<` on both ends preserves the original semantics
            of allowing back-to-back sessions (`10:00–11:00` and
            `11:00–12:00` don't conflict).
            """
            return (a.start_datetime < b.end_datetime
                    and b.start_datetime < a.end_datetime)

        for rec in self:
            for other in others:
                if is_faculty_constraint and rec.faculty_id \
                        and rec.faculty_id == other.faculty_id \
                        and _overlaps(rec, other):
                    raise ValidationError(_(
                        'You cannot create a session with same faculty'
                        ' on same date and time'))
                if is_classroom_constraint and rec.classroom_id \
                        and rec.classroom_id == other.classroom_id \
                        and _overlaps(rec, other):
                    raise ValidationError(_(
                        'You cannot create a session with same classroom'
                        ' on same date and time'))
                if rec not in need_batch_check:
                    continue
                if is_batch_and_subject_constraint \
                        and rec.batch_id == other.batch_id \
                        and rec.subject_id == other.subject_id \
                        and _overlaps(rec, other):
                    raise ValidationError(_(
                        'You cannot create a session for the same batch'
                        ' on same time and for same subject'))
                if is_batch_constraint \
                        and rec.batch_id == other.batch_id \
                        and _overlaps(rec, other):
                    raise ValidationError(_(
                        'You cannot create a session for the same batch'
                        ' on same time even if it is different subject'))

    @api.model_create_multi
    def create(self, values):
        records = super().create(values)
        # Auto-subscribe the initial follower set = faculty + student_ids.
        # `_sync_session_followers` uses `message_subscribe` (not a raw
        # sudo insert into mail.followers) so ACL is honoured and the
        # right default subtypes are attached — no more 'Discussions'
        # subtype lookup that failed silently on non-English installs.
        # Prefetch student_ids + faculty_id across the whole recordset
        # so the per-record `_session_follower_partners` reads batch
        # into one ORM query instead of N.
        records.mapped('student_ids.user_id.partner_id')
        records.mapped('faculty_id.user_id.partner_id')
        for record in records:
            record._sync_session_followers()
        return records

    # ── Follower auto-management ──────────────────────────────────────

    def _session_follower_partners(self):
        """Return the set of partners this session SHOULD have as
        followers right now: the faculty's user's partner + the
        partner of every student in ``student_ids`` who has a linked
        ``res.users``.

        Students / faculty without a login can't receive email, so
        they're silently skipped — subscribing partners without email
        addresses just creates dead followers.
        """
        self.ensure_one()
        partners = self.env['res.partner']
        if self.faculty_id and self.faculty_id.user_id:
            partners |= self.faculty_id.user_id.partner_id
        for student in self.student_ids:
            if student.user_id:
                partners |= student.user_id.partner_id
        return partners

    def _sync_session_followers(self):
        """Materialise the desired follower set on this record.

        On create: subscribes every partner in `_session_follower_partners`
        that isn't already a follower.

        On write (called with an old-vs-new diff from the write override
        below): unsubscribes partners that USED to qualify but no
        longer do (student removed from `student_ids`, faculty changed),
        and subscribes partners newly qualifying. Manual followers
        added via the chatter Follow button are LEFT ALONE.
        """
        self.ensure_one()
        desired = self._session_follower_partners()
        current = self.message_follower_ids.mapped('partner_id')
        to_add = desired - current
        if to_add:
            self.sudo().message_subscribe(partner_ids=to_add.ids)

    @api.onchange('course_id')
    def onchange_course(self):
        # Clear batch (batch belongs to a course — old batch is
        # invalid after a course swap) AND subject (a subject picked
        # under the OLD course is likely not in the NEW course's
        # subject list; without this the form kept the stale subject
        # even though the dropdown was re-scoped, and only the M2O
        # domain filter hinted at the mismatch).
        # Keep the subject only when the NEW course still includes it
        # (uncommon but valid — subjects are M2M-shared across courses).
        if self.course_id:
            course_subject_ids = self.course_id.subject_ids.ids
            if self.subject_id and self.subject_id.id not in course_subject_ids:
                self.subject_id = False
            self.batch_id = False
            return {
                'domain': {'subject_id': [('id', 'in', course_subject_ids)]}
            }
        # Course cleared → wipe dependent selections too.
        self.batch_id = False
        self.subject_id = False

    def notify_user(self):
        """Send ONE email per session to all followers with an email.

        Fixes three long-standing bugs in the previous implementation:

        1. **N+1 emails** — old code called ``send_mail`` once per
           follower per session (30 students + faculty ⇒ 31 sends).
           Now: single ``send_mail`` per session, all recipients on
           ``recipient_ids``. Odoo handles per-recipient rendering,
           unsubscribe tokens, and privacy internally.
        2. **Shared ``mail.template.partner_to`` mutation** — old code
           did ``template.partner_to = follower.partner_id.id`` inside
           the loop, mutating a DB-shared template row. Non-admin
           faculty confirming a session hit ``AccessError`` on the
           template write; concurrent writers raced. The mutation is
           gone entirely; recipients come through ``email_values``.
        3. **Cross-recipient privacy leak** — the template's static
           ``email_to = get_emails(followers)`` put every recipient's
           address in every other recipient's ``To:`` header. Now
           overridden to False so Odoo relies on ``recipient_ids``
           and each recipient sees only their own address.

        Also honours the ``dont_notify`` / ``no_calendar_sync``
        context flags used by bridge modules (Microsoft calendar
        sync, batch imports, etc.) that write to sessions purely
        for their own bookkeeping.
        """
        if self.env.context.get('dont_notify') \
                or self.env.context.get('no_calendar_sync'):
            return
        template = self.env.ref(
            'openeducat_timetable.session_details_changes',
            raise_if_not_found=False,
        )
        if not template:
            return
        for session in self:
            # Every follower whose partner has a non-empty email —
            # `.sudo()` because ACLs may block a follower's read of
            # someone else's partner record.
            partners = session.message_follower_ids.mapped('partner_id') \
                .sudo().filtered('email')
            if not partners:
                continue
            # Render timezone from the session organizer (faculty).
            # When one mail goes to N recipients we can only pick one
            # tz for the datetime format; the faculty's tz is the most
            # useful — they're the one who cares about "when am I
            # teaching" most acutely. Falls back to current user, then
            # UTC.
            organizer_user = session.faculty_id.user_id or self.env.user
            tz = organizer_user.tz or self.env.user.tz or 'UTC'
            template.with_context(timezone=tz).send_mail(
                session.id,
                email_values={
                    'recipient_ids': [(6, 0, partners.ids)],
                    # Zero out email_to so the template's static
                    # comma-joined follower list can't leak into the
                    # To: header. Odoo will use `recipient_ids` and
                    # produce one properly-addressed mail per partner.
                    'email_to': False,
                },
            )

    def get_emails(self, follower_ids):
        """Comma-joined follower emails, skipping followers without one.

        Retained for template backward compatibility (the shipped
        ``session_details_changes`` template references it in
        ``email_to``). ``notify_user`` overrides ``email_to`` to False
        so this string never actually reaches the wire, but keep the
        method well-behaved for any custom mail template a customer
        may have wired against it.
        """
        return ','.join(
            follower.sudo().partner_id.email
            for follower in follower_ids
            if follower.sudo().partner_id.email
        )

    def get_subject(self):
        return 'Lecture of ' + self.faculty_id.name + \
               ' for ' + self.subject_id.name + ' is ' + self.state

    # Fields whose change is worth emailing followers about — schedule
    # facts they'd want to know changed. Everything else (color tag,
    # active flag, stored-compute back-writes like user_ids, Microsoft
    # sync's microsoft_id write-back, etc.) is bookkeeping and should
    # NOT trigger a notification.
    _NOTIFY_WORTHY_FIELDS = frozenset({
        'state', 'start_datetime', 'end_datetime', 'faculty_id',
        'classroom_id', 'subject_id', 'batch_id', 'timing_id',
    })

    def write(self, vals):
        # If the write can change the auto-managed follower set —
        # faculty reassignment or a change to `student_ids` — snapshot
        # the OLD desired set now so we can diff after super() and
        # unsubscribe partners who no longer belong (student removed
        # from `student_ids`, or old faculty).
        _rebalance_watched = {'faculty_id', 'student_ids'}
        old_desired = {}
        # Snapshot the OLD student sets too so we can post a chatter
        # message per session describing exactly who was added or
        # removed and by whom. `mail.thread` field-level tracking on
        # a Many2many field would only give "list changed" without
        # naming individuals; a dedicated `message_post` produces a
        # readable audit-trail entry.
        old_students = {}
        if 'student_ids' in vals:
            for session in self:
                old_students[session.id] = session.student_ids
        if any(f in vals for f in _rebalance_watched):
            # Prefetch followers on the whole recordset in one query
            # before the per-session read below — Odoo's ORM prefetch
            # would do this too but we can force it explicitly and
            # avoid the fallback lazy-fetch per session.
            self.mapped('message_follower_ids.partner_id')
            for session in self:
                old_desired[session.id] = session._session_follower_partners()

        data = super().write(vals)

        # Only notify when the write actually changed something
        # followers care about. Previously every write to a
        # non-draft/done session fired an email — including trivial
        # edits (color/active) and stored-compute back-writes
        # (`user_ids` recompute, Microsoft sync's microsoft_id
        # write). Multi-email-per-Confirm was the visible symptom.
        should_notify = any(f in vals for f in self._NOTIFY_WORTHY_FIELDS)

        # Single pass: rebalance followers AND send notifications.
        to_notify = self.env['op.session']
        for session in self:
            old = old_desired.get(session.id)
            if old is not None:
                new = session._session_follower_partners()
                to_remove = old - new
                if to_remove:
                    session.sudo().message_unsubscribe(
                        partner_ids=to_remove.ids)
                # Subscribe newly qualifying partners.
                session._sync_session_followers()
            if session.id in old_students:
                session._log_student_ids_change(old_students[session.id])
            if should_notify and session.state not in ('draft', 'done'):
                to_notify |= session
        if to_notify:
            to_notify.notify_user()
        return data

    def _log_student_ids_change(self, old_students):
        """Post a chatter message enumerating student additions /
        removals so the session's audit trail shows who was moved
        in or out of a class and by whom.

        Called from `write()` when `student_ids` was in the vals.
        No-ops when the effective set is unchanged (a write of the
        same M2M list — e.g. via `(6, 0, [same ids])` — is common
        during onchange re-application and shouldn't spam the log).
        """
        self.ensure_one()
        old_ids = set(old_students.ids)
        new_ids = set(self.student_ids.ids)
        added = self.student_ids.filtered(lambda s: s.id not in old_ids)
        removed = old_students.filtered(lambda s: s.id not in new_ids)
        if not added and not removed:
            return
        actor = self.env.user.name or _('System')
        parts = []
        if added:
            parts.append(_(
                "%(actor)s added: %(names)s",
                actor=actor,
                names=', '.join(added.mapped('name')),
            ))
        if removed:
            parts.append(_(
                "%(actor)s removed: %(names)s",
                actor=actor,
                names=', '.join(removed.mapped('name')),
            ))
        # Plain-text body so translated multi-line stays legible in
        # the chatter. `message_type='comment'` puts it in the same
        # feed as user notes rather than the technical-log tab.
        self.message_post(
            body='<br/>'.join(parts),
            message_type='comment',
            subtype_xmlid='mail.mt_note',
        )

    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Sessions'),
            'template': '/openeducat_timetable/static/xls/op_session.xls'
        }]

    @api.model
    def _backfill_demo_student_ids(self):
        """Populate `student_ids` on demo sessions from their batch roster.

        Called from `demo/op_timetable_demo.xml` via a `<function>`
        tag — runs at demo-data-load time only (never on a real
        production install, since production runs with demo=off).

        The old post_init_hook ran on every install and had to guard
        against production; moving this into the demo XML makes the
        scope explicit: the demo file already only loads with demo,
        so this call inherits the same gate. On a fresh install with
        demo enabled, demo sessions come pre-populated with the demo
        batch's demo students. Idempotent — only touches sessions
        with an empty `student_ids`.
        """
        sessions = self.search([
            ('batch_id', '!=', False),
            ('student_ids', '=', False),
        ])
        if not sessions:
            return
        by_batch = {}
        for session in sessions:
            by_batch.setdefault(session.batch_id.id, self.browse())
            by_batch[session.batch_id.id] |= session
        enrollments = self.env['op.student.course'].search([
            ('batch_id', 'in', list(by_batch.keys())),
        ])
        students_by_batch = {}
        for enr in enrollments:
            students_by_batch.setdefault(
                enr.batch_id.id, self.env['op.student'])
            if enr.student_id:
                students_by_batch[enr.batch_id.id] |= enr.student_id
        for batch_id, batch_sessions in by_batch.items():
            students = students_by_batch.get(batch_id)
            if not students:
                continue
            batch_sessions.with_context(
                no_calendar_sync=True, dont_notify=True,
            ).write({'student_ids': [(6, 0, students.ids)]})
