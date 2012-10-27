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
from osv import osv
from osv import fields
class op_result_template(osv.osv):
    _name = 'op.result.template'
    _description = 'Result Template'

    _rec_name = 'exam_session_id'
    _columns = {
        'exam_session_id':fields.many2one('op.exam.session','Exam Session'),
        'name':fields.char("Name", size=254),
        'result_date':fields.date('Result Date'),
        'line_ids':fields.one2many('op.result.template.line', 'result_id', 'Lines'),

    }

op_result_template()

class op_result_template_line(osv.osv):
    _name = 'op.result.template.line'
    _description = 'Result template Line'

    _columns = {
        'exam_session_id':fields.many2one('op.exam.session','Exam Session'),
        'detailed_report':fields.boolean('Detailed Report'),
        'course_id': fields.related('exam_session_id', 'course_id', type='many2one', relation='op.course',
                            string='Course', readonly=True ),
        'batch_id': fields.related('exam_session_id', 'batch_id', type='many2one', relation='op.batch',
                            string='Batch', readonly=True ),
        'standard_id':fields.related('exam_session_id', 'standard_id', type='many2one',
                             relation='op.standard', string="Standard", readonly=True),
        'division_id': fields.related('exam_session_id', 'division_id', type='many2one', relation='op.division',
                            string='Division', readonly=True ),
        'result_id':fields.many2one('op.result.template','Result Template Line'),
        'exam_lines':fields.one2many('op.result.exam.line', 'result_id', 'Exam Lines'),
    }
    def onchange_exam_session(self, cr, uid, ids, exam_session_id, context={}):
        ret_val = {}

        return {'value':ret_val}

op_result_template_line()

class op_result_exam_line(osv.osv):
    _name = 'op.result.exam.line'
    _description = 'Result Exam Line'

    _columns = {
        'result_id':fields.many2one('op.result.template.line'),
        'exam_id':fields.many2one('op.exam', 'Exam'),
        'pass_marks':fields.related('exam_id', 'min_marks', type='float', string='Passing Marks', readonly=True),
        'total_marks':fields.related('exam_id', 'total_marks', type='float', string='Total Marks', readonly=True),
        'weightage':fields.float('Weightage'),
    }

op_result_exam_line()

