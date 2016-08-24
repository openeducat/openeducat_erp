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

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class OpVehicle(models.Model):
    _name = 'op.vehicle'

    name = fields.Char('Name', size=16, required=True)
    reg_number = fields.Char('Registration Number', size=16, required=True)
    capacity = fields.Integer('Capacity', required=True)
    active = fields.Boolean('Active', default=True)
    partner_id = fields.Many2one('res.partner', 'Driver')

    @api.constrains('capacity')
    def check_capacity(self):
        if self.capacity <= 0:
            raise ValidationError(_('Enter proper Capacity.'))
