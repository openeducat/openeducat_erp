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

class op_marksheet_line(osv.osv):
    _name = 'op.marksheet.line'
    _rec_name = 'marksheet_reg_id'
    
    _columns = {
            'marksheet_reg_id': fields.many2one('op.marksheet.register', string='Marksheet Register', required=True),
            'student_id': fields.many2one('op.student', string='Student', required=True),
            'result_line': fields.one2many('op.result', 'result_id', string='Result'),
    }
    
op_marksheet_line()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
