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

from odoo import models, api, fields, exceptions, _


class OpRoomDistribution(models.TransientModel):
    """ Exam Room Distribution """
    _name = "op.room.distribution"
    _description = "Room Distribution"

    @api.multi
    @api.depends('student_ids')
    def _compute_get_total_student(self):
        for record in self:
            total_student = 0
            if record.student_ids:
                total_student = len(record.student_ids)
            record.total_student = total_student

    @api.multi
    @api.depends('room_ids', 'room_ids.capacity')
    def _compute_get_room_capacity(self):
        for record in self:
            room_capacity = 0
            if record.room_ids:
                for room in record.room_ids:
                    room_capacity += (room.capacity or 0)
            record.room_capacity = room_capacity

    exam_id = fields.Many2one('op.exam', 'Exam(s)')
    subject_id = fields.Many2one('op.subject', 'Subject')
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
    student_ids = fields.Many2many("op.student", String='Student')

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

    @api.multi
    def schedule_exam(self):
        for exam in self:
            if exam.total_student > exam.room_capacity:
                raise exceptions.AccessError(
                    _("Room capacity must be greater than total number \
                      of student"))
            student_ids = []
            for student in exam.student_ids:
                student_ids.append(student.id)
            for room in exam.room_ids:
                for i in range(room.capacity):
                    if not student_ids:
                        continue
                    self.env['op.exam.attendees'].create({
                        'exam_id': exam.exam_id.id,
                        'student_id': student_ids[0],
                        'status': 'present',
                        'course_id': exam.course_id.id,
                        'batch_id': exam.batch_id.id,
                        'room_id': room.id
                    })
                    student_ids.remove(student_ids[0])
            exam.exam_id.state = 'schedule'
            return True
