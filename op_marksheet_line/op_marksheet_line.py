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
#   def _get_total(self, cr, uid, ids, name, args, context=None):
#       res = {}
#       for self_obj in self.browse(cr, uid, ids, context=context):
#           total = 0.0
#           per = 0.0
#           pass_flg = True
#           total_per = 0.0
#           number_fail = 0
#           for line in self_obj.result_line:
#               if line.status != 'p':
#                   pass_flg = False
#                   number_fail += 1
#               total+=line.marks
#               total_per += line.exam_id.total_marks

#           per = (total_per and (100/total_per)*total) or 0.0
#           result = ""

#           res_tmpl = self_obj.exam_session_id.result_id
#           if pass_flg and res_tmpl:
#               pass_st_ids = res_tmpl.pass_status_ids
#               to_consider = False
#               min_pass = 0.0

#               for pass_st in pass_st_ids:
#                   if pass_st.number <= per and pass_st.number > min_pass:
#                       min_pass = pass_st.number
#                       to_consider = pass_st

#               if to_consider:
#                   result  = to_consider.result
#           else:
#               if res_tmpl:
#                   crit_ids = res_tmpl.criteria_ids
#                   to_consider = False
#                   max_pass = False
#                   for crit_id in crit_ids:
#                       if crit_id.number == number_fail:
#                           to_consider = crit_id
#                       if not max_pass or  crit_id.number > max_pass.number:
#                           max_pass = crit_id
#                   if not to_consider:
#                       to_consider = max_pass
#                   result = to_consider.result


#           res[self_obj.id] = {
#               'total_marks': total,
#               'total_per': per,
#               'result':result,

#           }
#       return res
    _columns = {
            'marksheet_reg_id': fields.many2one('op.marksheet.register', string='Marksheet Register'),
            'exam_session_id':fields.many2one('op.result.template.line','Session Template'),
            'student_id': fields.many2one('op.student', string='Student', required=True),
            'result_line': fields.one2many('op.result.line', 'result_id', string='Result'),
            'total_marks':fields.float("Total Marks", ),
            'total_per':fields.float("Total Percentage",),
            'result':fields.char("Result", size=256),
    }

op_marksheet_line()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
