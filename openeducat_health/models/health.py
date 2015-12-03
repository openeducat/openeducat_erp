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


class OpHealth(models.Model):
    _name = 'op.health'
    _rec_name = 'student_id'
    _description = """Health Detail for Students and Faculties"""

    type = fields.Selection(
        [('student', 'Student'), ('faculty', 'Faculty')],
        'Type', default='student', required=True)
    student_id = fields.Many2one('op.student', 'Student')
    faculty_id = fields.Many2one('op.faculty', 'Faculty')
    height = fields.Float('Height(C.M.)', required=True)
    weight = fields.Float('Weight', required=True)
    blood_group = fields.Selection(
        [('A+', 'A+ve'), ('B+', 'B+ve'), ('O+', 'O+ve'), ('AB+', 'AB+ve'),
         ('A-', 'A-ve'), ('B-', 'B-ve'), ('O-', 'O-ve'), ('AB-', 'AB-ve')],
        'Blood Group', required=True)
    physical_challenges = fields.Boolean('Physical Challenge?', default=False)
    physical_challenges_note = fields.Text('Physical Challenge')
    major_diseases = fields.Boolean('Major Diseases?', default=False)
    major_diseases_note = fields.Text('Major Diseases')
    eyeglasses = fields.Boolean('Eye Glasses?')
    eyeglasses_no = fields.Char('Eye Glasses', size=64)
    regular_checkup = fields.Boolean(
        'Any Regular Checkup Required?', default=False)
    health_line = fields.One2many(
        'op.health.line', 'health_id', 'Checkup Lines')

    @api.constrains('height', 'weight')
    def check_height_weight(self):
        if self.height <= 0.0 or self.weight <= 0.0:
            raise ValidationError("Enter proper height and weight!")


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
