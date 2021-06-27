# -*- coding: utf-8 -*-
#/#############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2004-TODAY OpenEduCat Inc(<http://www.OpenEduCat Inc.com>).
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

class op_classroom(osv.osv):
    _name = 'op.classroom'

    _columns = {
            'name': fields.char(size=16, string='Name', required=True),
            'code': fields.char(size=4, string='Code', required=True),
            'course_id': fields.many2one('op.course', 'Course', required=True),
            'standard_id': fields.many2one('op.standard', 'Standard', required=True),
            'capacity': fields.integer(string='No. Of Person'),
            'facility': fields.many2many('op.facility', 'classroom_facility_rel', 'op_classroom_id', 'op_facility_id', string='Facilities'),
            'asset_line': fields.one2many('op.asset', 'asset_id', 'Asset', required=True),
    }

op_classroom()

class op_asset(osv.osv):
    _name = 'op.asset'
    
    _columns = {
                'asset_id': fields.many2one('op.classroom', 'Asset'),
                'product_id': fields.many2one('product.product', 'Product', required=True),
                'code': fields.char('Code', size=256),
                'product_uom_qty': fields.float('Quantity',required=True),
                
            }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
