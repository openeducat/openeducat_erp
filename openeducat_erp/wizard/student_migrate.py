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
from openerp.tools.translate import _
import time

class student_migrate(osv.osv_memory):
    """ Student Migration Wizard """

    _name = 'student.migrate'
    
    _columns = {
                'date': fields.date('Date', required=True),
                'course_id': fields.many2one('op.course', string='Course', required=True),
                'from_standard_id': fields.many2one('op.standard', string='From Standard', required=True),
                'to_standard_id': fields.many2one('op.standard', string='To Standard', required=True),
                'student_ids': fields.many2many('op.student', 'op_student_migration_rel', 
                                                'op_student_id', 'op_migrate_id', string='Student(s)', 
                                                required=True),
                }
    
    def _check_from_to_standard(self, cr, uid, ids, context=None):
        for self_obj in self.browse(cr, uid, ids): 
            if self_obj.from_standard_id.id == self_obj.to_standard_id.id:
                return False
        return True
    
    _constraints = [
        (_check_from_to_standard, 'Student is already in this standard.', ['from_standard_id','Can\'t Move']),
    ]
    
    def go_forward(self, cr, uid, ids, context={}):
        standard = self.pool.get("op.standard")
        activity = self.pool.get("op.activity")
        student_obj = self.pool.get("op.student")
        activity_type = self.pool.get("op.activity.type")
        lst_student =[]
        for self_obj in self.browse(cr, uid, ids):
            dic = {}
            act_type_id = activity_type.create(cr, uid, {'name': 'Migration'},context)
            for student in self_obj.student_ids:
                dic_act = {}
                dic_act = {
                           'student_id': student.id,
                           'type_id': act_type_id,
                           'date': self_obj.date
                           }
                act_id = activity.create(cr, uid, dic_act,context)
                student_std = student_obj.write(cr, uid, student.id, {'standard_id': self_obj.to_standard_id.id},context={} )
                lst_student.append(student.id)
            dic = {
                   'code': self_obj.to_standard_id.name,
                   'name': self_obj.to_standard_id.name,
                   'course_id': self_obj.course_id.id,
                   'date': self_obj.date,
                   'student_ids': [(6,0,lst_student)],
                   }
        std_id = standard.create(cr, uid, dic,context)
        
        value = {'type': 'ir.actions.act_window_close'}
        return value
        
student_migrate()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
