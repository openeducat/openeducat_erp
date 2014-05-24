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
class generate_roll_number(osv.osv_memory):
    _name = 'generate.roll.number'
    _description = 'Generate Roll Number'

    _columns = {
        'division_ids':fields.many2many('op.division','generate_roll_number_division', 'generate_id','division_id', 'Divisiones'),
        'type': fields.selection([('n','By Name'),
                                  ('s','By Surname'),
                                 ], 'Generation Sequence', required=True, ),
        'prefix':fields.char('Prefix',size=256, ),
        'sufix':fields.char('Sufix',size=256, ),
        'start':fields.integer('Number Starts from', required=True),
        'separator':fields.char('Separator',size=256,),
        'example':fields.char('Example',size=256, readonly=True),

    }
    def get_number(self, prefix, start, sufix, separator):

        example = ''
        if prefix:
            example += prefix + (separator or '')
        if start:
            example += str(start)

        if sufix:
            example += (separator or '' ) + sufix
        return example


    def onchange_number(self, cr, uid, ids, prefix, start, sufix, separator):

        ret_val = {'value':{'example':self.get_number(prefix, start, sufix, separator)}}
        return ret_val

    def act_generate(self, cr, uid, ids, context={}):
        student_pool = self.pool.get('op.student')
        roll_line_pool = self.pool.get('op.roll.number')
        standard_pool = self.pool.get('op.standard')
        std_obj = standard_pool.browse(cr, uid, context['active_id'], context=context)
        for self_obj in self.browse(cr, uid, ids, context=context):
            order_by = 'name,last_name,middle_name'
            if self_obj.type == 's':
                order_by = 'last_name,name,middle_name'


            division_ids = []

            if self_obj.division_ids:
                division_ids = [x.id for x in self_obj.division_ids]
            else:
                division_ids = [False]
            for div in division_ids:
                cond = [('standard_id','=',std_obj.id)]
                cond+=[('division_id','=',div)]
                stu_ids = student_pool.search(cr, uid, cond, context=context, order=order_by)
                roll_number = self_obj.start
                for stu_id in stu_ids:
                    stu_obj = student_pool.browse(cr, uid, stu_id, context=context)
                    roll_line_pool.create(cr, uid, {
                        'student_id':stu_id,
                        'batch_id':stu_obj.batch_id.id,
                        'standard_id':std_obj.id,
                        'course_id':std_obj.course_id.id,
                        'roll_number':self.get_number(self_obj.prefix, roll_number, self_obj.sufix, self_obj.separator)
                    })
                    roll_number += 1
        return {'type': 'ir.actions.act_window_close'}

generate_roll_number()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
