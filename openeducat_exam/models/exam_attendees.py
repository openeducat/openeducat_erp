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

from odoo import _, api, fields, models
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
    course_id = fields.Many2one('op.course', 'Course',
                                compute='_compute_exam_details',
                                store=True, readonly=True)
    batch_id = fields.Many2one('op.batch', 'Batch',
                               compute='_compute_exam_details',
                               store=True, readonly=True)
    room_id = fields.Many2one('op.exam.room', 'Room')

    _unique_attendees = models.Constraint('unique(student_id,exam_id)',
                                          'Attendee must be unique per exam.')

    @api.onchange('marks')
    def _onchange_marks(self):
        if self.exam_id:
            for attendee in self.exam_id.attendees_line:
                if attendee.marks not in (None, False):
                    self.exam_id.results_entered = True
                    return
            self.exam_id.results_entered = False

    @api.depends('exam_id')
    def _compute_exam_details(self):
        for record in self:
            if record.exam_id:
                record.course_id = record.exam_id.session_id.course_id.id
                record.batch_id = record.exam_id.session_id.batch_id.id
            else:
                record.course_id = False
                record.batch_id = False

    @api.onchange('exam_id')
    def onchange_exam(self):
        if self.exam_id:
            self.course_id = self.exam_id.session_id.course_id.id
            self.batch_id = self.exam_id.session_id.batch_id.id
        else:
            self.course_id = False
            self.batch_id = False
        self.student_id = False

    @api.constrains('marks', 'status')
    def _check_marks(self):
        for record in self:
            if record.status == 'present':
                if record.exam_id and (
                        record.marks < 0 or record.marks > record.exam_id.total_marks):
                    raise ValidationError(
                        _("Please Enter Marks between 0 and %d for a present student.")
                        % record.exam_id.total_marks)
            elif record.status == 'absent':
                if record.marks and record.marks != 0:
                    record.marks = 0
