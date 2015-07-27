# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from openerp import models, fields


class OpAttendanceLine(models.Model):
    _name = 'op.attendance.line'
    _rec_name = 'attendance_id'

    attendance_id = fields.Many2one(
        'op.attendance.sheet', 'Attendance', required=True)
    student_id = fields.Many2one('op.student', 'Student', required=True)
    present = fields.Boolean('Present ?')
    course_id = fields.Many2one(
        'op.course', 'Course', related='student_id.course_id', store=True,
        readonly=True)
    standard_id = fields.Many2one(
        'op.standard', 'Standard', related='student_id.standard_id',
        store=True, readonly=True)
    division_id = fields.Many2one(
        'op.division', 'Division', related='student_id.division_id',
        store=True, readonly=True)
    remark = fields.Char('Remark', size=256)
    attendance_date = fields.Date(
        'Date', related='attendance_id.attendance_date', store=True,
        readonly=True)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
