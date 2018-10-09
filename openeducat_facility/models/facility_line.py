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


class OpFacilityLine(models.Model):
    _name = "op.facility.line"
    _rec_name = "facility_id"
    _description = "Manage Facility Line"

    facility_id = fields.Many2one('op.facility', 'Facility', required=True)
    quantity = fields.Float('Quantity', required=True)

    @api.constrains('quantity')
    def check_quantity(self):
        if self.quantity <= 0.0:
            raise ValidationError(_("Enter proper Quantity in Facilities!"))
