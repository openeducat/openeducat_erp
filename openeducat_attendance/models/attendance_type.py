# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
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

from odoo import models, fields


class OpAttendanceType(models.Model):
    _name = "op.attendance.type"
    _inherit = ["mail.thread"]
    _description = "Attendance Type"

    name = fields.Char(
        'Name', size=20, required=True, tracking=True)
    active = fields.Boolean(default=True)
    present = fields.Boolean(
        'Present ?', tracking=True)
    excused = fields.Boolean(
        'Excused ?', tracking=True)
    absent = fields.Boolean('Absent', tracking=True)
    late = fields.Boolean('Late', tracking=True)
