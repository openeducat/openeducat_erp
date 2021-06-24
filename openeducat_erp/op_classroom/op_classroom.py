# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
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

from openerp import models, fields


class OpClassroom(models.Model):
    _name = 'op.classroom'

    name = fields.Char('Name', size=16, required=True)
    code = fields.Char('Code', size=4, required=True)
    course_id = fields.Many2one('op.course', 'Course', required=True)
    standard_id = fields.Many2one('op.standard', 'Standard', required=True)
    capacity = fields.Integer(string='No. Of Person')
    facility = fields.Many2many('op.facility', string='Facilities')
    asset_line = fields.One2many(
        'op.asset', 'asset_id', 'Asset', required=True)


class OpAsset(models.Model):
    _name = 'op.asset'

    asset_id = fields.Many2one('op.classroom', 'Asset')
    product_id = fields.Many2one('product.product', 'Product', required=True)
    code = fields.Char('Code', size=256)
    product_uom_qty = fields.Float('Quantity', required=True)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
