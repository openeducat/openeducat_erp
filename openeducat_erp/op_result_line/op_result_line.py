# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
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
###############################################################################

from openerp import models, fields


class OpResultLine(models.Model):
    _name = 'op.result.line'
    _rec_name = 'marks'

    marksheet_line_id = fields.Many2one(
        'op.marksheet.line', 'Marksheet Line')
    exam_id = fields.Many2one('op.exam', 'Exam', required=True)
    exam_tmpl_id = fields.Many2one('op.result.exam.line', 'Exam Template')
    marks = fields.Float('Marks', required=True)
    per = fields.Float('Percentage', required=True)
    student_id = fields.Many2one('op.student', 'Student', required=True)
    status = fields.Selection(
        [('p', 'Pass'), ('f', 'Fail')], 'Status', required=True)
    result_id = fields.Many2one('op.marksheet.line', 'MarkSheet Line')
    total_marks = fields.Float('Percentage')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
