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

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class OpMarksheetLine(models.Model):
    _name = 'op.marksheet.line'
    _rec_name = 'student_id'

    marksheet_reg_id = fields.Many2one(
        'op.marksheet.register', 'Marksheet Register')
    evaluation_type = fields.Selection(
        related='marksheet_reg_id.exam_session_id.evaluation_type', store=True)
    student_id = fields.Many2one('op.student', 'Student', required=True)
    result_line = fields.One2many(
        'op.result.line', 'marksheet_line_id', 'Results')
    total_marks = fields.Integer("Total Marks", compute='_compute_total_marks')
    percentage = fields.Float("Percentage", compute='_compute_percentage')
    grade = fields.Char('Grade', readonly=True, compute='_compute_grade')
    status = fields.Selection([('pass', 'Pass'), ('fail', 'Fail')], 'Status',
                              compute='_compute_status')

    @api.constrains('total_marks', 'percentage')
    def _check_marks(self):
        if (self.total_marks < 0.0) or (self.total_per < 0.0):
            raise ValidationError(_("Enter proper marks or percentage!"))

    @api.multi
    @api.depends('result_line.marks')
    def _compute_total_marks(self):
        for record in self:
            record.total_marks = sum([int(x.marks)
                                      for x in record.result_line])

    @api.multi
    @api.depends('total_marks')
    def _compute_percentage(self):
        for record in self:
            total_exam_marks = sum(
                [int(x.exam_id.total_marks) for x in record.result_line])
            record.percentage = record.total_marks and (
                100 * record.total_marks) / total_exam_marks or 0.0

    @api.multi
    @api.depends('percentage')
    def _compute_grade(self):
        for record in self:
            if record.evaluation_type == 'grade':
                grades = record.marksheet_reg_id.result_template_id.grade_ids
                for grade in grades:
                    if grade.min_per <= record.percentage and \
                            grade.max_per >= record.percentage:
                        record.grade = grade.result

    @api.multi
    @api.depends('result_line.status')
    def _compute_status(self):
        for record in self:
            record.status = 'pass'
            for result in record.result_line:
                if result.status == 'fail':
                    record.status = 'fail'
