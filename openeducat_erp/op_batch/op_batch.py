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

class op_batch(osv.osv):
    _name = 'op.batch'

    _columns = {
            'code': fields.char(size=8, string='Code', required=True),
            'name': fields.char(size=32, string='Name', required=True),
            'start_date': fields.date(string='Start Date', required=True),
            'end_date': fields.date(string='End Date', required=True),
            'course_id': fields.many2one('op.course', string='Course', required=True),
    }

op_batch()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
