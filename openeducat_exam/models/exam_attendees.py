# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
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

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class OpExamAttendees(models.Model):
    _name = "op.exam.attendees"
    _rec_name = "student_id"
    _description = "Exam Attendees"

    student_id = fields.Many2one('op.student', 'Student', required=True)
    status = fields.Selection(
        [('present', 'Present'), ('absent', 'Absent')],
        'Status', default="present", required=True)
    marks = fields.Integer('Marks')
    note = fields.Text('Note')
    exam_id = fields.Many2one(
        'op.exam', 'Exam', required=True, ondelete="cascade")
    course_id = fields.Many2one('op.course', 'Course', readonly=True)
    batch_id = fields.Many2one('op.batch', 'Batch', readonly=True)
    room_id = fields.Many2one('op.exam.room', 'Room')

    _sql_constraints = [
        ('unique_attendees',
         'unique(student_id,exam_id)',
         'Attendee must be unique per exam.'),
    ]

    @api.onchange('exam_id')
    def onchange_exam(self):
        self.course_id = self.exam_id.session_id.course_id
        self.batch_id = self.exam_id.session_id.batch_id
        self.student_id = False

    @api.constrains('marks')
    def _check_marks(self):
        if self.marks < 0.0:
            raise ValidationError(_("Enter proper marks!"))
