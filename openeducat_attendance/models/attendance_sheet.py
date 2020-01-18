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


class OpAttendanceSheet(models.Model):
    _name = "op.attendance.sheet"
    _inherit = ["mail.thread"]
    _description = "Attendance Sheet"
    _order = "attendance_date desc"

    @api.depends('attendance_line.present')
    def _compute_total_present(self):
        for record in self:
            record.total_present = self.env['op.attendance.line'].search_count(
                [('present', '=', True), ('attendance_id', '=', record.id)])

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
    active = fields.Boolean(default=True)

    state = fields.Selection(
        [('draft', 'Draft'), ('start', 'Attendance Start'),
         ('done', 'Attendance Taken'), ('cancel', 'Cancelled')],
        'Status', default='draft', track_visibility='onchange')

    def attendance_draft(self):
        self.state = 'draft'

    def attendance_start(self):
        self.state = 'start'

    def attendance_done(self):
        self.state = 'done'

    def attendance_cancel(self):
        self.state = 'cancel'

    _sql_constraints = [
        ('unique_register_sheet',
         'unique(register_id,session_id,attendance_date)',
         'Sheet must be unique per Register/Session.'),
    ]

    @api.model
    def create(self, vals):
        sheet = self.env['ir.sequence'].next_by_code('op.attendance.sheet')
        register = self.env['op.attendance.register']. \
            browse(vals['register_id']).code
        vals['name'] = register + sheet
        return super(OpAttendanceSheet, self).create(vals)
