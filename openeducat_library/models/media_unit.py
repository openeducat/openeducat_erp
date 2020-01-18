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

from odoo import models, fields, api


class OpMediaUnit(models.Model):
    _name = "op.media.unit"
    _inherit = "mail.thread"
    _description = "Media Unit"
    _order = "name"

    name = fields.Char('Name', required=True)
    media_id = fields.Many2one('op.media', 'Media',
                               required=True, track_visibility='onchange')
    barcode = fields.Char('Barcode', size=20)
    movement_lines = fields.One2many(
        'op.media.movement', 'media_unit_id', 'Movements')
    state = fields.Selection(
        [('available', 'Available'), ('issue', 'Issued')],
        'State', default='available', track_visibility='onchange')
    media_type_id = fields.Many2one(related='media_id.media_type_id',
                                    store=True, string='Media Type')
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('unique_name_barcode',
         'unique(barcode)',
         'Barcode must be unique per Media unit!'),
    ]

    @api.model
    def create(self, vals):
        x = self.env['ir.sequence'].next_by_code(
            'op.media.unit') or '/'
        vals['barcode'] = x
        return super(OpMediaUnit, self).create(vals)

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search(
                [('name', operator, name)] + args, limit=limit)
        if not recs:
            recs = self.search(
                [('barcode', operator, name)] + args, limit=limit)
        return recs.name_get()
