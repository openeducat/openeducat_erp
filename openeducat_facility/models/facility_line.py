# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
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


class OpFacilityLine(models.Model):
    _name = 'op.facility.line'
    _rec_name = 'facility_id'

    facility_id = fields.Many2one('op.facility', 'Facility', required=True)
    quantity = fields.Float('Quantity', required=True)

    @api.constrains('quantity')
    def check_quantity(self):
        if self.quantity <= 0.0:
            raise ValidationError(_("Enter proper Quantity in Facilities!"))
