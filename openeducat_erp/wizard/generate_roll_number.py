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

from openerp import models, fields, api


class GenerateRollNumber(models.TransientModel):
    _name = 'generate.roll.number'
    _description = 'Generate Roll Number'

    type = fields.Selection(
        [('n', 'By Name'), ('s', 'By Surname')], 'Generation Sequence',
        required=True)
    prefix = fields.Char('Prefix', size=256)
    start = fields.Integer('Number Starts from', required=True)
    sufix = fields.Char('Suffix', size=256)
    separator = fields.Char('Separator', size=256,)
    example = fields.Char('Example', size=256, readonly=True)
    division_ids = fields.Many2many('op.division', string='Divisions')

    def get_number(self, prefix, start, sufix, separator):
        example = ''
        if prefix:
            example += prefix + (separator or '')
        if start:
            example += str(start)
        if sufix:
            example += (separator or '') + sufix
        return example

    @api.onchange('prefix', 'start', 'sufix', 'separator')
    def onchange_number(self):
        self.example = self.get_number(
            self.prefix, self.start, self.sufix, self.separator)

    @api.one
    def act_generate(self):
        student_pool = self.env['op.student']
        std_obj = self.env['op.standard'].browse(
            self.env.context.get('active_id'))
        order_by = 'name,last_name,middle_name'
        if self.type == 's':
            order_by = 'last_name,name,middle_name'
        for div in self.division_ids:
            students = student_pool.search(
                [('standard_id', '=', std_obj.id),
                 ('division_id', '=', div.id)], order=order_by)
            roll_number = self.start
            for student in students:
                self.env['op.roll.number'].create({
                    'student_id': student.id,
                    'batch_id': student.batch_id.id,
                    'standard_id': std_obj.id,
                    'course_id': std_obj.course_id.id,
                    'roll_number': self.get_number(
                        self.prefix, roll_number,
                        self.sufix, self.separator)})
                roll_number += 1


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
