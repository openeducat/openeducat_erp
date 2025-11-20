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

import calendar

import pytz
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

week_days = [(calendar.day_name[0], (calendar.day_name[0])),
             (calendar.day_name[1], (calendar.day_name[1])),
             (calendar.day_name[2], (calendar.day_name[2])),
             (calendar.day_name[3], (calendar.day_name[3])),
             (calendar.day_name[4], (calendar.day_name[4])),
             (calendar.day_name[5], (calendar.day_name[5])),
             (calendar.day_name[6], (calendar.day_name[6]))]


class OpSession(models.Model):
    _name = "op.session"
    _inherit = ["mail.thread"]
    _description = "Sessions"

    name = fields.Char(compute='_compute_name', string='Name', store=True)
    timing_id = fields.Many2one(
        'op.timing', 'Timing', tracking=True)
    start_datetime = fields.Datetime(
        'Start Time', required=True,
        default=lambda self: fields.Datetime.now())
    end_datetime = fields.Datetime(
        'End Time', required=True)
    course_id = fields.Many2one(
        'op.course', 'Course', required=True)
    faculty_id = fields.Many2one(
        'op.faculty', 'Faculty', required=True)
    batch_id = fields.Many2one(
        'op.batch', 'Batch', required=True)
    subject_id = fields.Many2one(
        'op.subject', 'Subject', required=True)
    classroom_id = fields.Many2one(
        'op.classroom', 'Classroom')
    color = fields.Integer('Color Index')
    type = fields.Char(compute='_compute_day', string='Day', store=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirmed'),
         ('done', 'Done'), ('cancel', 'Canceled')],
        string='Status', default='draft')
    user_ids = fields.Many2many(
        'res.users', compute='_compute_batch_users',
        store=True, string='Users')
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

    @api.depends('start_datetime', 'end_datetime')
    def _compute_timing(self):
        tz = pytz.timezone(self.env.user.tz)
        for session in self:
            session.timing = str(
                session.start_datetime.astimezone(tz).strftime('%I:%M%p')
                ) + ' - ' + str(session.end_datetime.astimezone(
                    tz).strftime('%I:%M%p'))

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
        tz = pytz.timezone(self.env.user.tz)
        for session in self:
            if session.faculty_id and session.subject_id \
                    and session.start_datetime and session.end_datetime:
                session.name = \
                    session.faculty_id.name + ':' + \
                    session.subject_id.name + ':' + str(
                        session.start_datetime.astimezone(tz).strftime('%I:%M%p')) + '-' + str( # noqa
                        session.end_datetime.astimezone(tz).strftime('%I:%M%p'))

    # For record rule on student and faculty dashboard
    @api.depends('batch_id', 'faculty_id', 'user_ids.child_ids')
    def _compute_batch_users(self):
        student_obj = self.env['op.student']
        users_obj = self.env['res.users']
        for session in self:
            student_ids = student_obj.search(
                [('course_detail_ids.batch_id', '=', session.batch_id.id)])
            user_list = [student_id.user_id.id for student_id
                         in student_ids if student_id.user_id]
            if session.faculty_id.user_id:
                user_list.append(session.faculty_id.user_id.id)
            user_ids = users_obj.search([('child_ids', 'in', user_list)])
            if user_ids:
                user_list.extend(user_ids.ids)
            session.user_ids = user_list

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
        faculty_constraint = res_param.search([
            ('key', '=', 'timetable.is_faculty_constraint')])
        classroom_constraint = res_param.search([
            ('key', '=', 'timetable.is_classroom_constraint')])
        batch_and_subject_constraint = res_param.search([
            ('key', '=', 'timetable.is_batch_and_subject_constraint')])
        batch_constraint = res_param.search([
            ('key', '=', 'timetable.is_batch_constraint')])
        is_faculty_constraint = faculty_constraint.value
        is_classroom_constraint = classroom_constraint.value
        is_batch_and_subject_constraint = batch_and_subject_constraint.value
        is_batch_constraint = batch_constraint.value
        sessions = self.env['op.session'].search([])
        for session in sessions:
            for rec in self:
                if rec.id != session.id:
                    if is_faculty_constraint:
                        if rec.faculty_id.id == session.faculty_id.id and \
                                rec.start_datetime.date() == session.start_datetime.date() and ( # noqa
                                session.start_datetime.time() < rec.start_datetime.time() < session.end_datetime.time() or # noqa
                                session.start_datetime.time() < rec.end_datetime.time() < session.end_datetime.time() or # noqa
                                rec.start_datetime.time() <= session.start_datetime.time() < rec.end_datetime.time() or # noqa
                                rec.start_datetime.time() < session.end_datetime.time() <= rec.end_datetime.time()): # noqa
                            raise ValidationError(_(
                                'You cannot create a session'
                                ' with same faculty on same date '
                                'and time'))
                    if is_classroom_constraint:
                        if rec.classroom_id.id == session.classroom_id.id and \
                                rec.start_datetime.date() == session.start_datetime.date() and ( # noqa
                                session.start_datetime.time() < rec.start_datetime.time() < session.end_datetime.time() or # noqa
                                session.start_datetime.time() < rec.end_datetime.time() < session.end_datetime.time() or # noqa
                                rec.start_datetime.time() <= session.start_datetime.time() < rec.end_datetime.time() or # noqa
                                rec.start_datetime.time() < session.end_datetime.time() <= rec.end_datetime.time()): # noqa
                            raise ValidationError(_(
                                'You cannot create a session '
                                'with same classroom on same date'
                                ' and time'))
                    if is_batch_and_subject_constraint:
                        if rec.batch_id.id == session.batch_id.id and \
                                rec.start_datetime.date() == session.start_datetime.date() and ( # noqa
                                session.start_datetime.time() < rec.start_datetime.time() < session.end_datetime.time() or # noqa
                                session.start_datetime.time() < rec.end_datetime.time() < session.end_datetime.time() or # noqa
                                rec.start_datetime.time() <= session.start_datetime.time() < rec.end_datetime.time() or # noqa
                                rec.start_datetime.time() < session.end_datetime.time() <= rec.end_datetime.time()) and rec.subject_id.id == session.subject_id.id: # noqa
                            raise ValidationError(_(
                                'You cannot create a session '
                                'for the same batch on same time '
                                'and for same subject'))
                    if is_batch_constraint:
                        if rec.batch_id.id == session.batch_id.id and \
                                rec.start_datetime.date() == session.start_datetime.date() and ( # noqa
                                session.start_datetime.time() < rec.start_datetime.time() < session.end_datetime.time() or # noqa
                                session.start_datetime.time() < rec.end_datetime.time() < session.end_datetime.time() or # noqa
                                rec.start_datetime.time() <= session.start_datetime.time() < rec.end_datetime.time() or # noqa
                                rec.start_datetime.time() < session.end_datetime.time() <= rec.end_datetime.time()): # noqa
                            raise ValidationError(_(
                                'You cannot create a session for '
                                'the same batch on same time '
                                'even if it is different subject'))

    @api.model_create_multi
    def create(self, values):
        records = super(OpSession, self).create(values)
        for record in records:
            mfids = record.message_follower_ids
            partner_val = []
            partner_ids = []
            for val in mfids:
                partner_val.append(val.partner_id.id)
            if record.faculty_id and record.faculty_id.user_id:
                partner_ids.append(record.faculty_id.user_id.partner_id.id)
            if record.batch_id and record.course_id:
                course_val = self.env['op.student.course'].search([
                    ('batch_id', '=', record.batch_id.id),
                    ('course_id', '=', record.course_id.id)
                ])
                for val in course_val:
                    if val.student_id.user_id:
                        partner_ids.append(val.student_id.user_id.partner_id.id)
            subtype_id = self.env['mail.message.subtype'].sudo().search([
                ('name', '=', 'Discussions')])
            if partner_ids and subtype_id:
                mail_followers = self.env['mail.followers'].sudo()
                for partner in list(set(partner_ids)):
                    if partner in partner_val:
                        continue
                    mail_followers.create({
                        'res_model': record._name,
                        'res_id': record.id,
                        'partner_id': partner,
                        'subtype_ids': [[6, 0, [subtype_id[0].id]]]
                    })
        return records

    @api.onchange('course_id')
    def onchange_course(self):
        self.batch_id = False
        if self.course_id:
            subject_ids = self.env['op.course'].search([
                ('id', '=', self.course_id.id)]).subject_ids
            return {'domain': {'subject_id': [('id', 'in', subject_ids.ids)]}}

    def notify_user(self):
        for session in self:
            template = self.env.ref(
                'openeducat_timetable.session_details_changes',
                raise_if_not_found=False)
            for user in session.message_follower_ids:
                if user.sudo().partner_id:
                    template.partner_to = user.sudo().partner_id.id
                    context = dict(self.env.context)
                    user = self.env['res.users'].search([('partner_id', '=', user.sudo().partner_id.id)]) # noqa
                    context['timezone'] = user.tz or 'UTC'
                    template.with_context(context).send_mail(session.id)

    def get_emails(self, follower_ids):
        email_ids = ''
        for user in follower_ids:
            if email_ids:
                email_ids = email_ids + ',' + str(user.sudo().partner_id.email)
            else:
                email_ids = str(user.sudo().partner_id.email)
        return email_ids

    def get_subject(self):
        return 'Lecture of ' + self.faculty_id.name + \
               ' for ' + self.subject_id.name + ' is ' + self.state

    def write(self, vals):
        data = super(OpSession,
                     self.with_context(check_move_validity=False)).write(vals)
        for session in self:
            if session.state not in ('draft', 'done'):
                session.notify_user()
        return data

    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Sessions'),
            'template': '/openeducat_timetable/static/xls/op_session.xls'
        }]
