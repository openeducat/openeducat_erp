# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from openerp import models, fields


class OpResultExamLine(models.Model):
    _name = 'op.result.exam.line'
    _description = 'Result Exam Line'
    _rec_name = "exam_id"

    result_id = fields.Many2one('op.result.template.line', 'Session Template')
    exam_id = fields.Many2one('op.exam', 'Exam')
    pass_marks = fields.Float(
        'Passing Marks', related='exam_id.min_marks', readonly=True)
    total_marks = fields.Float(
        'Total Marks', related='exam_id.total_marks', readonly=True)
    weightage = fields.Float('Weightage')
    result_lines = fields.One2many(
        'op.result.line', 'exam_tmpl_id', 'Result Lines')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
