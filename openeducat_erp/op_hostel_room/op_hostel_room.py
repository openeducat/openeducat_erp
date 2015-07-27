# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from openerp import models, fields, api
from openerp.exceptions import ValidationError


class OpHostelRoom(models.Model):
    _name = 'op.hostel.room'

    hostel_id = fields.Many2one('op.hostel', 'Hostel')
#     name = fields.Char('Room Number', size=8, required=True),
    name = fields.Many2one('op.room', 'Name', required=True)
    student_ids = fields.Many2many('res.partner', string='Allocated Students ')
    students_per_room = fields.Integer('Students Per Room', required=True)
    rent = fields.Float('Rent')
    allocated_date = fields.Date('Allocated Date')
    facility_line = fields.One2many(
        'op.facility', 'hostel_room_id', 'Facilities')

    @api.onchange('name')
    def onchange_name(self):
        if self.name:
            self.students_per_room = self.name.capacity

    @api.one
    @api.constrains('student_ids', 'students_per_room')
    def _check_student_capacity(self):
        if len(self.student_ids) > self.students_per_room:
            raise ValidationError('Room capacity Over')


class OpRoom(models.Model):
    _name = 'op.room'

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)
    capacity = fields.Integer('Room Capacity', required=True)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
