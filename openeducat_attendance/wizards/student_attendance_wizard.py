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

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class StudentAttendance(models.TransientModel):
    _name = 'student.attendance'

    from_date = fields.Date(
        'From Date', required=True, default=lambda self: fields.Date.today())
    to_date = fields.Date(
        'To Date', required=True, default=lambda self: fields.Date.today())

    @api.one
    @api.constrains('from_date', 'to_date')
    def check_dates(self):
        from_date = fields.Date.from_string(self.from_date)
        to_date = fields.Date.from_string(self.to_date)
        if to_date < from_date:
            raise ValidationError(_("To Date cannot be set before From Date."))

    @api.multi
    def print_report(self):
        data = self.read(['from_date', 'to_date'])[0]
        data.update({'student_id': self.env.context.get('active_id', False)})

        return self.env['report'].get_action(
            self, 'openeducat_attendance.student_attendance_report', data=data)
