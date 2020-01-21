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

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class OpExamSession(models.Model):
    _name = "op.exam.session"
    _inherit = ["mail.thread"]
    _description = "Exam Session"

    name = fields.Char(
        'Exam Session', size=256, required=True, track_visibility='onchange')
    course_id = fields.Many2one(
        'op.course', 'Course', required=True, track_visibility='onchange')
    batch_id = fields.Many2one(
        'op.batch', 'Batch', required=True, track_visibility='onchange')
    exam_code = fields.Char(
        'Exam Session Code', size=16,
        required=True, track_visibility='onchange')
    start_date = fields.Date(
        'Start Date', required=True, track_visibility='onchange')
    end_date = fields.Date(
        'End Date', required=True, track_visibility='onchange')
    exam_ids = fields.One2many(
        'op.exam', 'session_id', 'Exam(s)')
    exam_type = fields.Many2one(
        'op.exam.type', 'Exam Type',
        required=True, track_visibility='onchange')
    evaluation_type = fields.Selection(
        [('normal', 'Normal'), ('grade', 'Grade')],
        'Evolution type', default="normal",
        required=True, track_visibility='onchange')
    venue = fields.Many2one(
        'res.partner', 'Venue', track_visibility='onchange')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('schedule', 'Scheduled'),
        ('held', 'Held'),
        ('cancel', 'Cancelled'),
        ('done', 'Done')
    ], 'State', default='draft', track_visibility='onchange')

    _sql_constraints = [
        ('unique_exam_session_code',
         'unique(exam_code)', 'Code should be unique per exam session!')]

    @api.constrains('start_date', 'end_date')
    def _check_date_time(self):
        if self.start_date > self.end_date:
            raise ValidationError(
                _('End Date cannot be set before Start Date.'))

    @api.onchange('course_id')
    def onchange_course(self):
        self.batch_id = False

    @api.multi
    def act_draft(self):
        self.state = 'draft'

    @api.multi
    def act_schedule(self):
        self.state = 'schedule'

    @api.multi
    def act_held(self):
        self.state = 'held'

    @api.multi
    def act_done(self):
        self.state = 'done'

    @api.multi
    def act_cancel(self):
        self.state = 'cancel'

    def search_read_for_exam(self, domain=None, fields=None, offset=0, limit=None, order=None):
        if self.env.user.partner_id.is_student:
            main_list = []
            user = self.env.user
            student = self.env['op.student'].sudo().search([('user_id','=',user.id)])
            values = [i.course_id.id for i in student.course_detail_ids]
            session = self.sudo().search([('course_id', 'in', values), ('state', 'not in', ['done', 'draft'])])

            for record in session:
                main_dict = {}
                main_dict.update({
                    'id': record.id,
                    'session_name': record.name,
                    'exam_type': record.exam_type.name,
                    'start_date': record.start_date,
                    'end_date': record.end_date,
                    'course_id': record.course_id.id
                })
                sub_list = []
                for exam in record.exam_ids:
                    sub_dict = {}
                    sub_dict.update({
                        'id': exam.id,
                        'session_id': exam.session_id.id,
                        'exam_name': exam.name,
                        'start_time': exam.start_time,
                        'end_time': exam.end_time,
                        'subject_name': exam.subject_id.name,
                        'status': exam.state,
                        'total_marks': exam.total_marks,
                        'passing_marks': exam.min_marks
                    })
                    min_list = []
                    for attendance in exam.attendees_line:
                        min_dict = {}
                        min_dict.update({'studnet_name': attendance.student_id.name})
                        min_list.append(min_dict)
                        sub_dict.update({'student': min_list})
                    sub_list.append(sub_dict)
                    main_dict.update({'exam': sub_list})
                main_list.append(main_dict, )
            return main_list
