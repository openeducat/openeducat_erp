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

class op_vehicle(osv.osv):
    _name = 'op.vehicle'

    _columns = {
            'name': fields.char(size=16, string='Name', required=True),
            'reg_number': fields.char(size=16, string='Registration Number', required=True),
            'capacity': fields.integer(string='Capacity', required=True),
            'active': fields.boolean(string='Active'),
    }

op_vehicle()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
