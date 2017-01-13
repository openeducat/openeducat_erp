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
from openerp import models, api, fields


class OpHeldExam(models.TransientModel):
    _name = 'op.held.exam'

    course_id = fields.Many2one('op.course', 'Course')
    batch_id = fields.Many2one('op.batch', 'Batch')
    exam_id = fields.Many2one('op.exam', 'Exam')
    subject_id = fields.Many2one('op.subject', 'Subject')
    attendees_line = fields.Many2many(
        'op.exam.attendees', string='Attendees')

    @api.model
    def default_get(self, fields):
        res = super(OpHeldExam, self).default_get(fields)
        active_id = self.env.context.get('active_id', False)
        exam = self.env['op.exam'].browse(active_id)
        session = exam.session_id
        res.update({
            'batch_id': session.batch_id.id,
            'course_id': session.course_id.id,
            'exam_id': active_id,
            'subject_id': exam.subject_id.id
        })
        return res

    @api.multi
    def held_exam(self):
        for record in self:
            if record.attendees_line:
                for attendee in record.attendees_line:
                    attendee.status = 'absent'
            record.exam_id.state = 'held'
            return True
