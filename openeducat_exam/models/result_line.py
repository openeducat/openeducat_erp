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

from openerp import models, fields, api
from openerp.exceptions import ValidationError


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
        [('pass', 'Pass'), ('fail', 'Fail')],
        'Status', default='pass', required=True)
    result_id = fields.Many2one('op.marksheet.line', 'Marksheet Line')
    total_marks = fields.Float('Total Marks')

    @api.constrains('marks', 'per')
    def _check_marks(self):
        if (self.marks < 0.0) or (self.per < 0.0) or \
                (self.total_marks < 0.0) or (self.per > 100.0):
            raise ValidationError("Enter proper Marks or Percentage!")
        elif self.marks > self.total_marks:
            raise ValidationError("Marks can't be greater than Total Marks")


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
