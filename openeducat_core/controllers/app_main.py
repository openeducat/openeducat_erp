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
from datetime import datetime
from odoo import http
import json
from odoo.http import request, Response
from odoo.addons.portal.controllers.web import \
    Home as home


class OpenEduCatAppController(http.Controller):

    @http.route(['/openeducat_core/get_app_dash_data'], type='http',
                auth='none', methods=['POST'], csrf=False)
    def compute_app_dashboard_data(self, **post):

        user_id = post.get('user_id', False)
        total_assignments = 0
        total_subs = 0
        today_lectures = 0
        assigned_books = 0
        total_exam = 0
        total_event = 0
        if user_id:
            ir_model = request.env['ir.model'].sudo()
            student = request.env['op.student'].sudo().search(
                [('user_id', '=', int(user_id))], limit=1)
            if student:
                assignment = ir_model.search([
                    ('model', '=', 'op.assignment')])
                if assignment:
                    total_assignments = request.env['op.assignment'] \
                        .sudo().search_count(
                        [('allocation_ids', 'in', student.id),
                         ('state', '=', 'publish')])
                    total_subs = request.env['op.assignment.sub.line'] \
                        .sudo().search_count(
                        [('student_id', '=', student.id),
                         ('state', '=', 'submit'), ('assignment_id.state', 'not in', ['finish'])])
                batch_ids = [x.batch_id.id for x in student.course_detail_ids]
                course_ids = [x.course_id.id for x in student.course_detail_ids]
                session = ir_model.search([('model', '=', 'op.session')])
                if session and batch_ids:
                    today_lectures = request.env['op.session'] \
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
                    assigned_books = request.env['op.media.movement'] \
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
                    total_exam = request.env['op.exam.session'].sudo().search_count(
                        [('course_id','in',values),('state', 'not in', ['done', 'draft'])])

                if student:
                    total_event = request.env['event.event'].sudo().search_count(
                        [('is_published', '=', True), ('state', 'not in', ['draft', 'done'])])

                apps = request.env['ir.module.module'].sudo().search(
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

        return Response(json.dumps(res,
                sort_keys=True, indent=4, ),
                content_type='application/json;charset=utf-8', status=200)

    @http.route(['/openeducat_core/get_parent_dash_data'], type='http',
                auth='none', methods=['POST'], csrf=False)
    def compute_parent_dashboard_data(self, **post):
        apps = request.env['ir.module.module'].sudo().search(
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
        return Response(json.dumps(res,
                sort_keys=True, indent=4, ),
                content_type='application/json;charset=utf-8', status=200)


    @http.route(['/openeducat_core/get_faculty_dash_data'], type='http',
                auth='none', methods=['POST'], csrf=False)
    def compute_faculty_dashboard_data(self, **post):
        user_id = post.get('user_id', False)
        total_assignments = 0
        total_subs = 0
        today_lectures = 0
        if user_id:
            faculty = request.env['op.faculty'].sudo().search([('user_id', '=', int(user_id))], limit=1)
            if faculty:
                ir_model = request.env['ir.model'].sudo()
                assignment = ir_model.search(
                    [('model', '=', 'op.assignment')])
                if assignment:
                    total_assignments = request.env['op.assignment'] \
                        .sudo().search_count(
                        [('faculty_id', '=', faculty.id),
                         ('state', 'in', ['draft', 'publish'])])
                    total_subs = request.env['op.assignment.sub.line'] \
                        .sudo().search_count(
                        [('assignment_id.faculty_id', '=', faculty.id),
                         ('state', '=', 'submit'), ('assignment_id.state', 'not in', ['finish'])])
                session = ir_model.search(
                    [('model', '=', 'op.session')])
                if session:
                    today_lectures = request.env['op.session'] \
                        .sudo().search_count(
                        [('state', 'not in', ['draft']),
                         ('faculty_id', '=', faculty.id),
                         ('start_datetime', '>=',
                          datetime.today().strftime('%Y-%m-%d 00:00:00')),
                         ('start_datetime', '<=',
                          datetime.today().strftime('%Y-%m-%d 23:59:59'))])

        apps = request.env['ir.module.module'].sudo().search(
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

        return Response(json.dumps(res,
                sort_keys=True, indent=4, ),
                content_type='application/json;charset=utf-8', status=200)


class OpeneducatHome(home):

    @http.route()
    def web_login(self, redirect=None, *args, **kw):
        response = super(OpeneducatHome, self).web_login(
            redirect=redirect, *args, **kw)
        if not redirect and request.params['login_success']:
            if request.env['res.users'].browse(request.uid).has_group(
                    'base.group_user'):
                redirect = b'/web?' + request.httprequest.query_string
            else:
                if request.env.user.is_parent:
                    redirect = '/my/child'
                else:
                    redirect = '/my/home'
            return http.redirect_with_hash(redirect)
        return response

    def _login_redirect(self, uid, redirect=None):
        if request.env.user.is_parent:
            return '/my/child'
        return '/my/home'
