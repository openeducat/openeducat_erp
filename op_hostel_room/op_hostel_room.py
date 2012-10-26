# -*- coding: utf-8 -*-
#/#############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2004-TODAY Tech-Receptives(<http://www.tech-receptives.com>).
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
#/#############################################################################
from osv import osv, fields

class op_hostel_room(osv.osv):
    _name = 'op.hostel.room'

    _columns = {
            'hostel_id': fields.many2one('op.hostel', string='Hostel', required=True),
            'name': fields.char(size=8, string='Room Number', required=True),
            'student_ids': fields.many2many('res.partner', 'student_hostel_room_rel', 'op_hostel_room_id', 'res_partner_id', string='Allocated Students '),
            'students_per_room': fields.integer(string='Students Per Room', required=True),
            'rent': fields.float(string='Rent', required=True),
            'allocated_date': fields.date(string='Allocated Date'),
    }

op_hostel_room()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
