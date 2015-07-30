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


class OpHostel(models.Model):
    _name = 'op.hostel'

    name = fields.Char('Name', size=16, required=True)
    capacity = fields.Integer('Hostel Capacity', required=True)
#     room_ids = fields.Many2many('op.hostel.room', string='Room(s)')
    room_lines = fields.One2many('op.hostel.room', 'hostel_id', 'Room(s)')
#     rooms = fields.Integer('Rooms', required=True)

    @api.one
    @api.constrains('room_lines')
    def _check_hostel_capacity(self):
        counter = 0.00
        for room in self.room_lines:
            counter += room.students_per_room
            if counter > self.capacity:
                raise ValidationError('Hostel Capacity Over')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
