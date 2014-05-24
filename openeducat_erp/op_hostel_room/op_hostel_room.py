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

class op_hostel_room(osv.osv):
    _name = 'op.hostel.room'

    _columns = {
            'hostel_id': fields.many2one('op.hostel', string='Hostel'),
#            'name': fields.char(size=8, string='Room Number', required=True),
            'name': fields.many2one('op.room', 'Name', required=True),   
            'student_ids': fields.many2many('res.partner', 'student_hostel_room_rel', 'op_hostel_room_id', 'res_partner_id', string='Allocated Students '),
            'students_per_room': fields.integer(string='Students Per Room', required=True),
            'rent': fields.float(string='Rent'),
            'allocated_date': fields.date(string='Allocated Date'),
            'facility_line': fields.one2many('op.facility', 'hostel_room_id', 'Facilities')
    }
    
    
    
    def onchange_name(self, cr, uid, ids, room, context={}):
        res = {}
        if room:
            res = {
                   'students_per_room': self.pool.get('op.room').browse(cr, uid, room).capacity,
                   }
        return {'value': res}
    
    
    def _check_student_capacity(self, cr, uid, ids, context=None):
        for self_obj in self.browse(cr, uid, ids):
            counter = 0.00
            for student in self_obj.student_ids:
                counter += 1
                if counter > self_obj.students_per_room:
                    return False
        return True
    
    _constraints = [
        (_check_student_capacity, 'Room capacity Over.', ['Capacity Over']),
    ]
    
    
    
op_hostel_room()


class op_room(osv.osv):
    
    _name = 'op.room'
    
    _columns = {
                'name': fields.char('Name', required=True),
                'code': fields.char('Code', required=True),
                'capacity': fields.integer('Room Capacity', required=True),
                }
op_room()    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
