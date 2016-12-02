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
from odoo.exceptions import UserError
from ..models import media_unit


class ReturnMedia(models.TransientModel):

    """ Retrun Media Wizard """
    _name = 'return.media'

    media_id = fields.Many2one('op.media', 'Media', readonly=True)
    media_unit_id = fields.Many2one(
        'op.media.unit', 'Media Unit', readonly=True, required=True)
    actual_return_date = fields.Date(
        'Actual Return Date', default=lambda self: fields.Date.today(),
        required=True)

    @api.one
    def do_return(self):
        if self.media_unit_id.state and self.media_unit_id.state == 'issue':
            media_move_search = self.env['op.media.movement'].search(
                [('media_unit_id', '=', self.media_unit_id.id),
                 ('state', '=', 'issue')])
            if not media_move_search:
                raise UserError(_("Can't return media."))
                return {'type': 'ir.actions.act_window_close'}
            media_move_search.return_media(self.actual_return_date)
        else:
            raise UserError(_(
                "Media Unit can not be returned because it's state is : %s") %
                (dict(media_unit.unit_states).get(self.media_unit_id.state)))
