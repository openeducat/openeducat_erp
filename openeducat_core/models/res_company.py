# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
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

from odoo import models, fields, api
from _datetime import datetime


class ResCompany(models.Model):
    _inherit = "res.company"

    signature = fields.Binary('Signature')
    accreditation = fields.Text('Accreditation')
    approval_authority = fields.Text('Approval Authority')


class ResUsers(models.Model):
    _inherit = "res.users"

    user_line = fields.One2many('op.student', 'user_id', 'User Line')
    child_ids = fields.Many2many(
        'res.users', 'res_user_first_rel1',
        'user_id', 'res_user_second_rel1', string='Childs')

    @api.multi
    def create_user(self, records, user_group=None):
        for rec in records:
            if not rec.user_id:
                user_vals = {
                    'name': rec.name,
                    'login': rec.email or (rec.name + rec.last_name),
                    'partner_id': rec.partner_id.id
                }
                user_id = self.create(user_vals)
                rec.user_id = user_id
                if user_group:
                    user_group.users = user_group.users + user_id

    def search_read_for_app(self, domain=None, fields=None, offset=0, limit=None, order=None):
        if self.env.user.partner_id.is_student:
            domain = ([('user_id', '=', self.env.user.id)])
            user = self.sudo().search_read(domain=domain, fields=['name', 'email', 'image',
                                                                  'mobile', 'country_id', 'city', 'street', 'state_id',
                                                                  'zip'], offset=offset, limit=limit, order=order)
            student = self.env['op.student'].sudo().search([('user_id', '=', self.env.user.id)])
            res = {'user_data': user,
                   'birth_date': student.birth_date,
                   'blood_group': student.blood_group,
                   'gender': student.gender,
                   'student_id': student.id
                   }
            return res

        elif self.env.user.partner_id.is_parent:
            domain = ([('user_id', '=', self.env.user.id)])
            res = self.sudo().search_read(domain=domain, fields=['name', 'email', 'image', 'mobile', 'country_id',
                                                                 'city', 'street', 'state_id', 'zip'], offset=offset,
                                          limit=limit, order=order)
            return {'user_data': res}

        else:
            domain = ([('user_id', '=', self.env.user.id)])
            user = self.sudo().search_read(domain=domain, fields=['name', 'email', 'image', 'mobile', 'country_id',
                                                                  'city', 'street', 'state_id', 'zip'],
                                           offset=offset, limit=limit, order=order)
            faculty = self.env['op.faculty'].sudo().search([('user_id', '=', self.env.user.id)])
            res = {'user_data': user,
                   'faculty_id': faculty.id,
                   'birth_date': faculty.birth_date,
                   'blood_group': faculty.blood_group,
                   'gender': faculty.gender}
            return res

    def compute_student_dashboard_data(self, kw=[]):

        user_id = kw
        total_assignments = 0
        total_subs = 0
        today_lectures = 0
        assigned_books = 0
        total_exam = 0
        total_event = 0
        if user_id:
            ir_model = self.env['ir.model'].sudo()
            student = self.env['op.student'].sudo().search(
                [('user_id', '=', user_id)], limit=1)
            if student:
                assignment = ir_model.search([
                    ('model', '=', 'op.assignment')])
                if assignment:
                    total_assignments = self.env['op.assignment'] \
                        .sudo().search_count(
                        [('allocation_ids', 'in', student.id),
                         ('state', '=', 'publish')])
                    total_subs = self.env['op.assignment.sub.line'] \
                        .sudo().search_count(
                        [('student_id', '=', student.id),
                         ('state', '=', 'submit'), ('assignment_id.state', 'not in', ['finish'])])
                batch_ids = [x.batch_id.id for x in student.course_detail_ids]
                course_ids = [x.course_id.id for x in student.course_detail_ids]
                session = ir_model.search([('model', '=', 'op.session')])
                if session and batch_ids:
                    today_lectures = self.env['op.session'] \
                        .sudo().search_count(
                        [('state', 'not in', ['draft']),
                         ('batch_id', 'in', batch_ids),
                         ('start_datetime', '>=',
                          datetime.today().strftime('%Y-%m-%d 00:00:00')),
                         ('start_datetime', '<=',
                          datetime.today().strftime('%Y-%m-%d 23:59:59'))])
                library = ir_model.search([
                    ('model', '=', 'op.media.movement')])
                if library:
                    assigned_books = self.env['op.media.movement'] \
                        .sudo().search_count([
                        ('student_id', '=', student.id),
                        ('state', '=', 'issue')])
                if student:
                    values = []
                    for record in student.course_detail_ids:
                        values.append(record.course_id.id)

                exam_session = ir_model.search([
                    ('model', '=', 'op.exam.session')])
                if exam_session:
                    total_exam = self.env['op.exam.session'].sudo().search_count(
                        [('course_id','in',values),('state', 'not in', ['done', 'draft'])])

                events = ir_model.sudo().search_count(
                    [('model', '=', 'event.event')])
                if events:
                    total_event = self.env['event.event'].sudo().search_count([('state', 'not in', ['draft', 'done'])])

                apps = self.env['ir.module.module'].sudo().search(
                    ['|', '|', '|', '|', '|', ('name', '=', 'openeducat_exam'),
                     ('name', '=', 'openeducat_assignment'),
                     ('name', '=', 'openeducat_timetable'),
                     ('name', '=', 'openeducat_attendance'),
                     ('name', '=', 'openeducat_library'),
                     ('name', '=', 'openeducat_alumni_event_enterprise')
                     ])

                assignment = ''
                library = ''
                exam = ''
                attendance = ''
                event = ''
                timetable = ''

                app_name = []
                for i in apps:
                    app_name.append(i.name)

                    if 'openeducat_assignment' == i.name:
                        assignment = i.state
                    if 'openeducat_library' == i.name:
                        library = i.state
                    if 'openeducat_exam' == i.name:
                        exam = i.state
                    if 'openeducat_attendance' == i.name:
                        attendance = i.state
                    if 'openeducat_alumni_event_enterprise' == i.name:
                        event = i.state
                    if 'openeducat_timetable' == i.name:
                        timetable = i.state

        res = {
            'student_id':student.id,
            'course_ids': course_ids,
            'assignment': {
                'name': 'Assignments',
                'state': assignment,
                'count': total_assignments,
            },
            'submission': {
                'name': 'Submissions',
                'state': assignment,
                'count': total_subs,
            },
            'library': {
                'name': 'Library',
                'state': library,
                'count': assigned_books,
            },
            'attendance': {
                'name': 'Attendance',
                'state': attendance,
                'count': '',
            },
            'exam': {
                'name': 'Exam & Result',
                'state': exam,
                'count': total_exam,
            },
            'event': {
                'name': 'Events',
                'state': event,
                'count': total_event,
            },
            'timetable': {
                'name': 'Time Table',
                'state': timetable,
                'count': today_lectures,
            },
        }
        return  res


    def compute_faculty_dashboard_data(self, kw=[]):
        user_id = kw
        total_assignments = 0
        total_subs = 0
        today_lectures = 0
        if user_id:
            faculty = self.env['op.faculty'].sudo().search([('user_id', '=', user_id)], limit=1)
            if faculty:
                ir_model = self.env['ir.model'].sudo()
                assignment = ir_model.search(
                    [('model', '=', 'op.assignment')])
                if assignment:
                    total_assignments = self.env['op.assignment'] \
                        .sudo().search_count(
                        [('faculty_id', '=', faculty.id),
                         ('state', 'in', ['draft', 'publish'])])
                    total_subs = self.env['op.assignment.sub.line'] \
                        .sudo().search_count(
                        [('assignment_id.faculty_id', '=', faculty.id),
                         ('state', '=', 'submit'), ('assignment_id.state', 'not in', ['finish'])])
                session = ir_model.search(
                    [('model', '=', 'op.session')])
                if session:
                    today_lectures = self.env['op.session'] \
                        .sudo().search_count(
                        [('state', 'not in', ['draft']),
                         ('faculty_id', '=', faculty.id),
                         ('start_datetime', '>=',
                          datetime.today().strftime('%Y-%m-%d 00:00:00')),
                         ('start_datetime', '<=',
                          datetime.today().strftime('%Y-%m-%d 23:59:59'))])

        apps = self.env['ir.module.module'].sudo().search(
            ['|', '|',
             ('name', '=', 'openeducat_assignment'),
             ('name', '=', 'openeducat_timetable'),
             ('name', '=', 'openeducat_attendance')
             ])

        assignment = ''
        attendance = ''
        timetable = ''

        app_name = []
        for i in apps:
            app_name.append(i.name, )

            if 'openeducat_assignment' == i.name:
                assignment = i.state
            if 'openeducat_attendance' == i.name:
                attendance = i.state
            if 'openeducat_timetable' == i.name:
                timetable = i.state

        res = {
            'faculty_id':faculty.id,
            'assignment': {
                'name': 'Assignments',
                'state': assignment,
                'count': total_assignments,
            },
            'submission': {
                'name': 'Submissions',
                'state': assignment,
                'count': total_subs,
            },
            'attendance': {
                'name': 'Attendance',
                'state': attendance,
                'count': '',
            },
            'timetable': {
                'name': 'Time Table',
                'state': timetable,
                'count': today_lectures,
            }
        }
        return res

    def compute_parent_dashboard_data(self, kw=[]):
        apps = self.env['ir.module.module'].sudo().search(
            ['|', '|', '|',
             ('name', '=', 'openeducat_exam'),
             ('name', '=', 'openeducat_assignment'),
             ('name', '=', 'openeducat_timetable'),
             ('name', '=', 'openeducat_attendance')
             ])

        assignment = ''
        exam = ''
        attendance = ''
        timetable = ''

        app_name = []
        for i in apps:
            app_name.append(i.name, )

            if 'openeducat_assignment' == i.name:
                assignment = i.state
            if 'openeducat_exam' == i.name:
                exam = i.state
            if 'openeducat_attendance' == i.name:
                attendance = i.state
            if 'openeducat_timetable' == i.name:
                timetable = i.state

        res = {
            'assignment': {
                'name': 'Assignments',
                'state': assignment,
                'count': '',
            },
            'submission': {
                'name': 'Submissions',
                'state': assignment,
                'count': '',
            },
            'attendance': {
                'name': 'Attendance',
                'state': attendance,
                'count': '',
            },
            'exam': {
                'name': 'Exam & Result',
                'state': exam,
                'count': '',
            },
            'timetable': {
                'name': 'Time Table',
                'state': timetable,
                'count': '',
            }
        }
        return res