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
from openerp.osv import osv, fields

class op_hostel(osv.osv):
    _name = 'op.hostel'

    _columns = {
            'name': fields.char(size=16, string='Name', required=True),
            'capacity': fields.integer('Hostel Capacity', required=True),
#            'room_ids': fields.many2many('op.hostel.room', 'hostel_id','room_id', 'hostel_room_id_rel','Room(s)'),
            'room_lines': fields.one2many('op.hostel.room','hostel_id', 'Room(s)')
#            'rooms': fields.integer(string='Rooms', required=True),
        }
    
    def _check_hostel_capacity(self, cr, uid, ids, context=None):
        for self_obj in self.browse(cr, uid, ids):
            counter = 0.00
            for room in self_obj.room_lines:
                counter += room.students_per_room
                if counter > self_obj.capacity:
                    return False
        return True
    
    _constraints = [
        (_check_hostel_capacity, 'Hostel capacity Over.', ['Capacity Over']),
    ]
            

op_hostel()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
