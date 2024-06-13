# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<https://www.openeducat.org>).
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

from odoo import models,_, fields, api
from odoo.exceptions import ValidationError


class OpClassroom(models.Model):
    _name = "op.classroom"
    _description = "Classroom"

    name = fields.Char('Name', size=16, required=True)
    code = fields.Char('Code', size=16, required=True)
    course_id = fields.Many2one('op.course', 'Course')
    batch_id = fields.Many2one('op.batch', 'Batch')
    capacity = fields.Integer(string='No of Person')
    facilities = fields.One2many('op.facility.line', 'classroom_id',
                                 string='Facility Lines')
    asset_line = fields.One2many('op.asset', 'asset_id',
                                 string='Asset')
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('unique_classroom_code',
         'unique(code)', 'Code should be unique per classroom!'),
        ('unique_classroom_name',
         'unique(name)', 'Classroom name must be unique!')
        ]

    @api.onchange('course_id')
    def onchange_course(self):
        self.batch_id = False

    @api.constrains('asset_line','capacity')
    def check_quantity(self):
        for record in self:
            if record.asset_line.product_uom_qty < 0.0:
                raise ValidationError(_("Product's quantity must be positive"))
            if record.capacity < 0:
                raise ValidationError(_("Number of Person must be positive"))
