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

class op_scholarship(osv.osv):
    _name = 'op.scholarship'
    
    _columns = {
            'name': fields.char(size=64, string='Name', required=True),
            'student_id': fields.many2one('op.student', 'Student', required=True),
            'type_id': fields.many2one('op.scholarship.type','Type', required=True),
            'state': fields.selection([('d','Draft'),('c','Confirm'),('r','Reject')],readonly=True ,select=True, string='State')
    }
    
    def act_draft(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'d'})
        return True
    
    def act_confirm(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'c'})
        return True
    
    def act_reject(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'r'})
        return True
    
op_scholarship()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
