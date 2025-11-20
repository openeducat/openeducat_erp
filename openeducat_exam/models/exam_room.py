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

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class OpExamRoom(models.Model):
    _name = "op.exam.room"
    _description = "Exam Room"

    name = fields.Char('Name', size=256, required=True)
    classroom_id = fields.Many2one('op.classroom', 'Classroom', required=True)
    capacity = fields.Integer(
        'No of Seats', related="classroom_id.capacity", store=True)

    @api.constrains('capacity')
    def check_capacity(self):
        for rec in self:
            if rec.capacity < 0:
                raise ValidationError(_('Enter proper Capacity'))
            elif rec.capacity > rec.classroom_id.capacity:
                raise ValidationError(_('Capacity over Classroom capacity!'))

    @api.onchange('classroom_id')
    def onchange_classroom(self):
        if self.classroom_id:
            self.capacity = self.classroom_id.capacity
