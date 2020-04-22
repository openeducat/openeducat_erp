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

from odoo import models, fields


class OpAttendanceLine(models.Model):
    _name = "op.attendance.line"
    _inherit = ["mail.thread"]
    _rec_name = "attendance_id"
    _description = "Attendance Lines"
    _order = "attendance_date desc"

    attendance_id = fields.Many2one(
        'op.attendance.sheet', 'Attendance Sheet', required=True,
        track_visibility="onchange", ondelete="cascade")
    student_id = fields.Many2one(
        'op.student', 'Student', required=True, track_visibility="onchange")
    present = fields.Boolean(
        'Present ?', default=True, track_visibility="onchange")
    course_id = fields.Many2one(
        'op.course', 'Course',
        related='attendance_id.register_id.course_id', store=True,
        readonly=True)
    batch_id = fields.Many2one(
        'op.batch', 'Batch',
        related='attendance_id.register_id.batch_id', store=True,
        readonly=True)
    remark = fields.Char('Remark', size=256, track_visibility="onchange")
    attendance_date = fields.Date(
        'Date', related='attendance_id.attendance_date', store=True,
        readonly=True, track_visibility="onchange")
    register_id = fields.Many2one(
        related='attendance_id.register_id', store=True)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('unique_student',
         'unique(student_id,attendance_id,attendance_date)',
         'Student must be unique per Attendance.'),
    ]
