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

class op_publisher(osv.osv):
    _name = 'op.publisher'
    
    _columns = {
            'name': fields.char(size=128, string='Name', required=True),
            'address_id': fields.many2one('res.partner.address', string='Address'),
            'book_ids': fields.many2many('op.book', 'book_publisher_rel', 'op_publisher_id', 'op_book_id', string='Publisher'),
    }
    
op_publisher()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
