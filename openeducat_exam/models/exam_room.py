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


class OpExamRoom(models.Model):
    _name = 'op.exam.room'

    name = fields.Char('Name', size=256, required=True)
    classroom_id = fields.Many2one('op.classroom', 'Classroom', required=True)
    capacity = fields.Integer('Capacity', required=True)

    @api.constrains('capacity')
    def check_capacity(self):
        if self.capacity < 0:
            raise ValidationError(_('Enter proper Capacity'))
        elif self.capacity > self.classroom_id.capacity:
            raise ValidationError(_('Capacity over Classroom capacity!'))

    @api.onchange('classroom_id')
    def onchange_classroom(self):
        self.capacity = self.classroom_id.capacity
