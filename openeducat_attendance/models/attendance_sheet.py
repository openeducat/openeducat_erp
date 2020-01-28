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

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class OpAttendanceSheet(models.Model):
    _name = "op.attendance.sheet"
    _inherit = ["mail.thread"]
    _description = "Attendance Sheet"
    _order = "attendance_date desc"

    @api.multi
    @api.depends('attendance_line.present')
    def _compute_total_present(self):
        for record in self:
            record.total_present = self.env['op.attendance.line'].search_count(
                [('present', '=', True), ('attendance_id', '=', record.id)])

    @api.multi
    @api.depends('attendance_line.present')
    def _compute_total_absent(self):
        for record in self:
            record.total_absent = self.env['op.attendance.line'].search_count(
                [('present', '=', False), ('attendance_id', '=', record.id)])

    name = fields.Char('Name', readonly=True, size=32)
    register_id = fields.Many2one(
        'op.attendance.register', 'Register', required=True,
        track_visibility="onchange")
    course_id = fields.Many2one(
        'op.course', related='register_id.course_id', store=True,
        readonly=True)
    batch_id = fields.Many2one(
        'op.batch', 'Batch', related='register_id.batch_id', store=True,
        readonly=True)
    session_id = fields.Many2one('op.session', 'Session')
    attendance_date = fields.Date(
        'Date', required=True, default=lambda self: fields.Date.today(),
        track_visibility="onchange")
    attendance_line = fields.One2many(
        'op.attendance.line', 'attendance_id', 'Attendance Line')
    total_present = fields.Integer(
        'Total Present', compute='_compute_total_present',
        track_visibility="onchange")
    total_absent = fields.Integer(
        'Total Absent', compute='_compute_total_absent',
        track_visibility="onchange")
    faculty_id = fields.Many2one('op.faculty', 'Faculty')

    state = fields.Selection(
        [('draft', 'Draft'), ('start', 'Attendance Start'),
         ('done', 'Attendance Taken'), ('cancel', 'Cancelled')],
        'Status', default='draft', track_visibility='onchange')

    @api.multi
    def attendance_draft(self):
        self.state = 'draft'

    @api.multi
    def attendance_start(self):
        self.state = 'start'

    @api.multi
    def attendance_done(self):
        self.state = 'done'

    @api.multi
    def attendance_cancel(self):
        self.state = 'cancel'

    _sql_constraints = [
        ('unique_register_sheet',
         'unique(register_id,session_id,attendance_date)',
         'Sheet must be unique per Register/Session.'),
    ]

    @api.model
    def create(self, vals):
        sheet = self.env['ir.sequence'].sudo().next_by_code('op.attendance.sheet')
        register = self.env['op.attendance.register']. \
            browse(int(vals['register_id']))
        vals['name'] = register.code + sheet
        res = super(OpAttendanceSheet, self).create(vals)
        return res

    def new_create_attendance_lines(self, kw=[]):
        sheet_id = kw
        if sheet_id:
            attend_lines = self.env['op.attendance.line'].sudo()
            sheet = self.env['op.attendance.sheet'].sudo().browse(
                sheet_id)
            all_student_search = self.env['op.student'].sudo().search(
                [('course_detail_ids.course_id', '=',
                  sheet.register_id.course_id.id),
                 ('course_detail_ids.batch_id', '=',
                  sheet.register_id.batch_id.id)])
            attendance_lines = attend_lines.search(
                [('attendance_id', '=', sheet.id)])
            a = [x.id for x in all_student_search]
            b = [x.student_id.id for x in attendance_lines]
            remaining_students = set(a).difference(b)
            for student in remaining_students:
                attend_lines.create({
                    'attendance_id': sheet.id,
                    'student_id': student,
                    'attendance_date': fields.Date.today(),
                    'present': True
                })
        return True
