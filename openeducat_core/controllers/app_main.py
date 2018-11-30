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
from odoo.http import request


class OpenEduCatAppController(http.Controller):

    @http.route(['/openeducat_core/get_app_dash_data'], type='json',
                auth='none', methods=['POST'], csrf=False)
    def compute_app_dashboard_data(self, **post):
        user_id = post.get('user_id', False)
        total_assignments = 0
        total_subs = 0
        today_lectures = 0
        assigned_books = 0

        if user_id:
            student = request.env['op.student'].sudo().search(
                [('user_id', '=', user_id)], limit=1)
            if student:
                assignment = request.env['ir.model'].sudo().search(
                    [('model', '=', 'op.assignment')])
                if assignment:
                    total_assignments = request.env['op.assignment'] \
                        .sudo().search_count(
                        [('allocation_ids', 'in', student.id),
                         ('state', '=', 'publish')])
                    total_subs = request.env['op.assignment.sub.line'] \
                        .sudo().search_count(
                        [('student_id', '=', student.id),
                         ('state', '=', 'submit')])

                batch_ids = [x.batch_id.id for x in student.course_detail_ids]
                session = request.env['ir.model'].sudo().search(
                    [('model', '=', 'op.session')])
                if session and batch_ids:
                    today_lectures = request.env['op.session'] \
                        .sudo().search_count(
                        [('batch_id', 'in', batch_ids),
                         ('start_datetime', '>=',
                          datetime.today().strftime('%Y-%m-%d 00:00:00')),
                         ('start_datetime', '<=',
                          datetime.today().strftime('%Y-%m-%d 23:59:59'))])

                library = request.env['ir.model'].sudo().search(
                    [('model', '=', 'op.media.movement')])
                if library:
                    assigned_books = request.env['op.media.movement'] \
                        .sudo().search_count(
                        [('student_id', '=', student.id),
                         ('state', '=', 'issue')])

        return {'total_assignments': total_assignments,
                'total_submissions': total_subs,
                'today_lectures': today_lectures,
                'assigned_books': assigned_books}

    @http.route(['/openeducat_core/get_faculty_dash_data'], type='json',
                auth='none', methods=['POST'], csrf=False)
    def compute_faculty_dashboard_data(self, **post):
        user_id = post.get('user_id', False)
        total_assignments = 0
        total_subs = 0
        today_lectures = 0

        if user_id:
            faculty = request.env['op.faculty'].sudo().search(
                [('user_id', '=', user_id)], limit=1)
            if faculty:
                assignment = request.env['ir.model'].sudo().search(
                    [('model', '=', 'op.assignment')])
                if assignment:
                    total_assignments = request.env['op.assignment'] \
                        .sudo().search_count(
                        [('faculty_id', '=', faculty.id),
                         ('state', 'in', ['draft', 'publish'])])
                    total_subs = request.env['op.assignment.sub.line'] \
                        .sudo().search_count(
                        [('assignment_id.faculty_id', '=', faculty.id),
                         ('state', '=', 'submit')])

                session = request.env['ir.model'].sudo().search(
                    [('model', '=', 'op.session')])
                if session:
                    today_lectures = request.env['op.session'] \
                        .sudo().search_count(
                        [('faculty_id', '=', faculty.id),
                         ('start_datetime', '>=',
                          datetime.today().strftime('%Y-%m-%d 00:00:00')),
                         ('start_datetime', '<=',
                          datetime.today().strftime('%Y-%m-%d 23:59:59'))])

        return {'total_assignments': total_assignments,
                'total_submissions': total_subs,
                'today_lectures': today_lectures, }
