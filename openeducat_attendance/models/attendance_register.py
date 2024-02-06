# -*- coding: utf-8 -*-
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

from odoo import models, fields, api


class OpAttendanceRegister(models.Model):
    _name = "op.attendance.register"
    _inherit = ["mail.thread"]
    _description = "Attendance Register"
    _order = "id DESC"

    name = fields.Char(
        'Name', size=16, required=True, tracking=True)
    code = fields.Char(
        'Code', size=16, required=True, tracking=True)
    course_id = fields.Many2one(
        'op.course', 'Course', required=True, tracking=True)
    batch_id = fields.Many2one(
        'op.batch', 'Batch', required=True, tracking=True)
    subject_id = fields.Many2one(
        'op.subject', 'Subject', tracking=True)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('unique_attendance_register_code',
         'unique(code)', 'Code should be unique per attendance register!')]

    @api.depends('course_id')
    def onchange_course(self):
        if not self.course_id:
            self.batch_id = False
