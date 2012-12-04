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
from tools.translate import _
import time

class student_migrate(osv.osv_memory):
    """ Student Migration Wizard """

    _name = 'student.migrate'
    
    _columns = {
                'course_id': fields.many2one('op.course', string='Course', required=True),
                'from_standard_id': fields.many2one('op.standard', string='From Standard', required=True),
                'to_standard_id': fields.many2one('op.standard', string='To Standard', required=True),
                'student_ids': fields.many2many('op.student', 'op_student_migration_rel', 
                                                'op_student_id', 'op_migrate_id', string='Student(s)', 
                                                required=True),
                }
    
    def go_forward(self, cr, uid, ids, context={}):
        standard = self.pool.get("op.standard")
        lst_student =[]
        for self_obj in self.browse(cr, uid, ids):
            dic = {}
            for student in self_obj.student_ids:
                lst_student.append(student.id)
            dic = {
                   'code': self_obj.to_standard_id.name,
                   'name': self_obj.to_standard_id.name,
                   'course_id': self_obj.course_id.id,
                   'student_ids': [(6,0,lst_student)],
                   }
        std_id = standard.create(cr, uid, dic,context)
        value = {'type': 'ir.actions.act_window_close'}
        return value

student_migrate()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
