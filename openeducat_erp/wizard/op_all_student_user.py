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

from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
from bsddb.dbtables import _columns
from openerp.osv.orm import except_orm

class wizard_op_student(osv.osv):
    
    _name = 'wizard.op.student'
    _description = "Create User the selected Students"
    
    def _get_students(self, cr, uid, context=None):
        if not context:
            context = {}
            
        if context and context.get("active_ids"):
            return context.get("active_ids")
        return []
    
    _columns = {
               'student_ids': fields.many2many('op.student', 'ref_student_user_wiz', "student_id", "user_id", "Students"),
        }
            
    def create_user(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        active_ids = context.get('active_ids', []) or []
        ir_model_data = self.pool.get("ir.model.data")
        student_pool = self.pool.get('op.student')
        
        user_obj = self.pool.get('res.users')
        user_fields = user_obj.fields_get(cr, uid, context=context)
        user_default = user_obj.default_get(cr, uid, user_fields, context=context)
        user_default_group_lst = user_default['groups_id']
        student_group_id = ir_model_data.get_object_reference(cr, uid, 'openeducat_erp', 'group_op_student')[1]
        user_default_group_lst[0][2].append(student_group_id)
        user_default['groups_id'] = user_default_group_lst
        for stud in student_pool.browse(cr, uid, active_ids, context=context):
            if not stud.user_id:
                user_vals = {
                        'name' : stud.name,
                        'login' : stud.name,
                        'partner_id':stud.partner_id.id,                    
                }
                user_default.update(user_vals)
                user_id = self.pool.get('res.users').create(cr, uid, user_default, context=context)
                student_pool.write(cr, uid, [stud.id], {'user_id': user_id}, context=context)
        return {'type': 'ir.actions.act_window_close'}
    
    _defaults = {
                 'student_ids' : _get_students,
                 }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
        
    