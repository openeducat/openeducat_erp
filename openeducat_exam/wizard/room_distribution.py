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
from openerp import models, api, fields, exceptions, _


class OpRoomDistribution(models.TransientModel):

    """ Exam Room Distribution """
    _name = 'op.room.distribution'

    @api.one
    @api.depends('student_ids')
    def _get_total_student(self):
        total_student = 0
        if self.student_ids:
            total_student = len(self.student_ids)
        self.total_student = total_student

    @api.one
    @api.depends('room_ids', 'room_ids.capacity')
    def _get_room_capacity(self):
        room_capacity = 0
        if self.room_ids:
            for room in self.room_ids:
                room_capacity += (room.capacity or 0)
        self.room_capacity = room_capacity

    exam_id = fields.Many2one('op.exam', 'Exam')
    subject_id = fields.Many2one('op.subject', 'Subject')
    name = fields.Char("Exam")
    start_time = fields.Datetime("Start Time")
    end_time = fields.Datetime("End Time")
    exam_session = fields.Many2one("op.exam.session", 'Exam Session')
    course_id = fields.Many2one("op.course", 'Course')
    batch_id = fields.Many2one("op.batch", 'Batch')
    total_student = fields.Integer(
        "Total Student", compute="_get_total_student")
    room_capacity = fields.Integer(
        "Room Capacity", compute="_get_room_capacity")
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

    @api.one
    def schedule_exam(self):
        if self.total_student > self.room_capacity:
            raise exceptions.AccessError(
                _("Room capacity must be greater than total number \
                  of student"))
        student_ids = []
        for student in self.student_ids:
            student_ids.append(student.id)
        for room in self.room_ids:
            for i in range(room.capacity):
                if not student_ids:
                    continue
                self.env['op.exam.attendees'].create({
                    'exam_id': self.exam_id.id,
                    'student_id': student_ids[0],
                    'status': 'present',
                    'course_id': self.course_id.id,
                    'batch_id': self.batch_id.id,
                    'room_id': room.id
                })
                student_ids.remove(student_ids[0])
        self.exam_id.state = 'schedule'
        return True
