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

from openerp import models, fields


class OpRoom(models.Model):
    _name = 'op.room'

    hostel_id = fields.Many2one('op.hostel', 'Hostel', required=True)
    name = fields.Char('Room Name', required=True)
    code = fields.Char('Code', required=True)
    capacity = fields.Integer('Room Capacity', required=True)
    facility_line = fields.One2many('op.facility.line', 'room_id', 'Facility')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
