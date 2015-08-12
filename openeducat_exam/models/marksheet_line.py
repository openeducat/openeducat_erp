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


class OpMarksheetLine(models.Model):
    _name = 'op.marksheet.line'
    _rec_name = 'student_id'

    marksheet_reg_id = fields.Many2one(
        'op.marksheet.register', 'Marksheet Register')
    exam_session_id = fields.Many2one(
        'op.result.template.line', 'Session Template')
    student_id = fields.Many2one('op.student', 'Student', required=True)
    result_line = fields.One2many('op.result.line', 'result_id', 'Result')
    total_marks = fields.Float("Total Marks")
    total_per = fields.Float("Total Percentage")
    result = fields.Char("Result", size=256)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
