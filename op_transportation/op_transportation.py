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

class op_transportation(osv.osv):
    _name = 'op.transportation'
    
    _columns = {
            'name': fields.char(size=64, string='Name', required=True),
            'stop': fields.one2many('op.stop', 'transport_id', 'Stop'),
            'vehicle_id': fields.many2one('op.vehicle', 'Vehicle', required=True),
            'start_time': fields.datetime(string='Start Time', required=True),
            'end_time': fields.datetime(string='End Time', required=True),
            'from':fields.char(string="From", size=20, required=True),
            'to':fields.char(string="To", size=20, required=True),
            'student_ids': fields.many2many('op.student', 'student_transport_rel', 'op_student_id', 'transport_id', string='Add Student(s)'),
    }

op_transportation()


class op_stop(osv.osv):
    _name = 'op.stop'
    
    _columns = {
            
            'name': fields.char(size=64, string='Name', required=True),
            'sequence': fields.integer('Sequence'),
            'transport_id': fields.many2one('op.transportation', 'Transport'),
    }
    
    _order = 'sequence asc'
op_stop()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
