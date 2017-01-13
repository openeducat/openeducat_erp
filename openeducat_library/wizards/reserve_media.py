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


class ReserveMedia(models.TransientModel):

    """ Reserve Media """
    _name = 'reserve.media'

    partner_id = fields.Many2one('res.partner', required=True)

    @api.multi
    def set_partner(self):
        for media in self:
            self.env['op.media.movement'].browse(
                self.env.context.get('active_ids', False)).write(
                {'partner_id': media.partner_id.id,
                 'reserver_name': media.partner_id.name, 'state': 'reserve'})
