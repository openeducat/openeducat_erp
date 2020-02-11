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


class OpLibraryCardType(models.Model):
    _name = "op.library.card.type"
    _description = "Library Card Type"

    name = fields.Char('Name', size=256, required=True)
    allow_media = fields.Integer('No of medias Allowed', size=10,
                                 required=True)
    duration = fields.Integer(
        'Duration', help='Duration in terms of Number of Lead Days',
        required=True)
    penalty_amt_per_day = fields.Float('Penalty Amount per Day',
                                       required=True)

    @api.constrains('allow_media', 'duration', 'penalty_amt_per_day')
    def check_details(self):
        if self.allow_media < 0 or self.duration < 0.0 or \
                self.penalty_amt_per_day < 0.0:
            raise ValidationError(_('Enter proper value'))


class OpLibraryCard(models.Model):
    _name = "op.library.card"
    _rec_name = "number"
    _description = "Library Card"

    partner_id = fields.Many2one(
        'res.partner', 'Student/Faculty', required=True)
    number = fields.Char('Number', size=256, readonly=True)
    library_card_type_id = fields.Many2one(
        'op.library.card.type', 'Card Type', required=True)
    issue_date = fields.Date(
        'Issue Date', required=True, default=fields.Date.today())
    type = fields.Selection(
        [('student', 'Student'), ('faculty', 'Faculty')],
        'Type', default='student', required=True)
    student_id = fields.Many2one('op.student', 'Student',
                                 domain=[('library_card_id', '=', False)])
    faculty_id = fields.Many2one('op.faculty', 'Faculty',
                                 domain=[('library_card_id', '=', False)])
    active = fields.Boolean(default=True)

    _sql_constraints = [(
        'unique_library_card_number',
        'unique(number)',
        'Library card Number should be unique per card!')]

    @api.model
    def create(self, vals):
        x = self.env['ir.sequence'].next_by_code(
            'op.library.card') or '/'
        vals['number'] = x
        res = super(OpLibraryCard, self).create(vals)
        if res.type == 'student':
            res.student_id.library_card_id = res
        else:
            res.faculty_id.library_card_id = res
        return res

    @api.onchange('type')
    def onchange_type(self):
        self.student_id = False
        self.faculty_id = False
        self.partner_id = False

    @api.onchange('student_id', 'faculty_id')
    def onchange_student_faculty(self):
        if self.student_id:
            self.partner_id = self.student_id.partner_id
        if not self.student_id and self.faculty_id:
            self.partner_id = self.faculty_id.partner_id
