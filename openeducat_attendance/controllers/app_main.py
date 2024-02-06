# -*- coding: utf-8 -*-
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

from odoo import http, fields
from odoo.http import request


class OpAttendanceController(http.Controller):

    @http.route(['/openeducat-attendance/take-attendance'], type='json',
                auth='none', methods=['POST'], csrf=False)
    def create_attendance_lines(self, **post):
        sheet_id = post.get('attendance_sheet_id', False)
        if sheet_id:
            attend_lines = request.env['op.attendance.line'].sudo()
            sheet = request.env['op.attendance.sheet'].sudo().browse(
                [sheet_id])
            all_student_search = request.env['op.student'].sudo().search(
                [('course_detail_ids.course_id', '=',
                  sheet.register_id.course_id.id),
                 ('course_detail_ids.batch_id', '=',
                  sheet.register_id.batch_id.id)])
            attendance_lines = attend_lines.search(
                [('attendance_id', '=', sheet.id)])
            a = [x.id for x in all_student_search]
            b = [x.student_id.id for x in attendance_lines]
            remaining_students = set(a).difference(b)
            for student in remaining_students:
                attend_lines.create({
                    'attendance_id': sheet.id,
                    'student_id': student,
                    'attendance_date': fields.Date.today(),
                    'present': True
                })
        return True
