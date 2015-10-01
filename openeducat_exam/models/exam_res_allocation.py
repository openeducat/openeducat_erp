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

from openerp import models, fields, api


class OpExamResAllocation(models.Model):
    _name = 'op.exam.res.allocation'

    exam_session_ids = fields.Many2many(
        'op.exam.session', string='Select Exam Session')
    exam_ids = fields.Many2many('op.exam', string='Exam(s)')
    faculty_ids = fields.Many2many('op.faculty', string='Faculty')
    student_ids = fields.Many2many('op.student', string='Student')

    @api.onchange('exam_session_ids')
    def onchange_exam_session_res(self):
        for session in self.exam_session_ids:
            students = self.env['op.student'].search(
                [('course_id', '=', session.course_id.id)])
            self.exam_ids = session.exam_ids.ids
            self.student_ids = students.ids

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
