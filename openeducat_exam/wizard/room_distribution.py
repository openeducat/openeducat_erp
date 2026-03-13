###############################################################################
#
#    openEMIS
#    Copyright (C) 2009-TODAY openEMIS(<https://www.openemis.org>).
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

from odoo import _, api, exceptions, fields, models
from odoo.exceptions import ValidationError


class OpRoomDistribution(models.TransientModel):
    """ Exam Room Distribution """
    _name = "op.room.distribution"
    _description = "Room Distribution"

    @api.depends('student_ids')
    def _compute_get_total_student(self):
        for record in self:
            total_student = 0
            if record.student_ids:
                total_student = len(record.student_ids)
            record.total_student = total_student

    @api.depends('room_ids', 'room_ids.capacity')
    def _compute_get_room_capacity(self):
        for record in self:
            room_capacity = 0
            if record.room_ids:
                for room in record.room_ids:
                    room_capacity += (room.capacity or 0)
            record.room_capacity = room_capacity

    exam_id = fields.Many2one('op.exam', 'Exam(s)')
    subject_id = fields.Many2one('op.subject', 'Subject',
                                 related="exam_id.subject_id")
    name = fields.Char("Exam")
    start_time = fields.Datetime("Start Time")
    end_time = fields.Datetime("End Time")
    exam_session = fields.Many2one("op.exam.session", 'Exam Session')
    course_id = fields.Many2one("op.course", 'Course')
    batch_id = fields.Many2one("op.batch", 'Batch')
    total_student = fields.Integer(
        "Total Student", compute="_compute_get_total_student")
    room_capacity = fields.Integer(
        "Room Capacity", compute="_compute_get_room_capacity")
    room_ids = fields.Many2many("op.exam.room", string="Exam Rooms")
    student_ids = fields.Many2many("op.student", string='Student')

    @api.model
    def default_get(self, fields):
        res = super(OpRoomDistribution, self).default_get(fields)
        active_id = self.env.context.get('active_id', False)
        exam = self.env['op.exam'].browse(active_id)
        session = exam.session_id
        reg_ids = self.env['op.subject.registration'].search(
            [('course_id', '=', session.course_id.id)])
        student_ids = []
        for reg in reg_ids:
            if exam.subject_id.subject_type == 'compulsory':
                student_ids.append(reg.student_id.id)
            else:
                for sub in reg.elective_subject_ids:
                    if sub.id == exam.subject_id.id:
                        student_ids.append(reg.student_id.id)
        student_ids = list(set(student_ids))
        total_student = len(student_ids)
        res.update({
            'exam_id': active_id,
            'name': exam.name,
            'start_time': exam.start_time,
            'end_time': exam.end_time,
            'exam_session': session.id,
            'course_id': session.course_id.id,
            'batch_id': session.batch_id.id,
            'total_student': total_student,
            'student_ids': [(6, 0, student_ids)],
        })
        return res

    def schedule_exam(self):
        attendance_model = self.env['op.exam.attendees']
        if not self.room_ids or not self.student_ids:
            raise ValidationError(
                _("Please Enter both Room And student"))

        non_conflict_exam_states = ['done', 'cancel', 'draft', 'result_updated']
        existing_attendees_for_this_exam = attendance_model.search([
            ('exam_id', '=', self.exam_id.id)
        ])
        if existing_attendees_for_this_exam:
            existing_attendees_for_this_exam.unlink()
        booked_rooms = attendance_model.search([
            ('room_id', 'in', self.room_ids.ids),
            ('exam_id.start_time', '<', self.end_time),
            ('exam_id.end_time', '>', self.start_time),
            ('exam_id.state', 'not in', non_conflict_exam_states),
            ('exam_id', '!=', self.exam_id.id)
        ])

        if booked_rooms:
            booked_room_names = ', '.join(booked_rooms.mapped('room_id.name'))
            raise ValidationError(
                _("The selected rooms (%s) are already booked for the specified "
                  "time by other active exams.") % booked_room_names)

        conflicting_students = attendance_model.search([
            ('student_id', 'in', self.student_ids.ids),
            ('exam_id.start_time', '<', self.end_time),
            ('exam_id.end_time', '>', self.start_time),
            ('exam_id.state', 'not in', non_conflict_exam_states),
            ('exam_id', '!=', self.exam_id.id)
        ])

        if conflicting_students:
            conflicting_student_names = ', '.join(
                conflicting_students.mapped('student_id.name'))
            raise ValidationError(
                _("Students (%s) are already scheduled for another active exam "
                  "during the specified time.") % conflicting_student_names)

        for exam_wiz in self:
            if exam_wiz.total_student > exam_wiz.room_capacity:
                raise exceptions.AccessError(
                    _("Room capacity must be greater than total number of student"))

            student_ids_to_assign = list(exam_wiz.student_ids.ids)

            for room in exam_wiz.room_ids:
                assigned_in_room = 0
                room_current_capacity = room.capacity

                while student_ids_to_assign and \
                        assigned_in_room < room_current_capacity:
                    student_id = student_ids_to_assign.pop(0)
                    attendance_model.create({
                        'exam_id': exam_wiz.exam_id.id,
                        'student_id': student_id,
                        'status': 'present',
                        'course_id': exam_wiz.course_id.id,
                        'batch_id': exam_wiz.batch_id.id,
                        'room_id': room.id
                    })
                    assigned_in_room += 1
            exam_wiz.exam_id.state = 'schedule'
            self.exam_id.results_entered = False
            return True
