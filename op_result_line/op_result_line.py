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

class op_result_line(osv.osv):
    _name = 'op.result.line'
    _rec_name = 'marks'

    _columns = {
            'marksheet_line_id': fields.many2one('op.marksheet.line', string='Marksheet Line'),
            'exam_id': fields.many2one('op.exam', string='Exam', required=True),
            'exam_tmpl_id':fields.many2one('op.result.exam.line','Exam Template'),
            'marks': fields.float(string='Marks', required=True),
            'per': fields.float(string='Percentage', required=True),
            'student_id': fields.many2one('op.student', string='Student', required=True),
            'status': fields.selection([('p','Pass'),('f','Fail')], string='Status', required=True),
            'result_id':fields.many2one('op.marksheet.line','MarkSheet Line'),
            'total_marks': fields.float(string='Percentage'),
    }

op_result_line()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
