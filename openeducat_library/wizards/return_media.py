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

from odoo import models, fields, _
from odoo.exceptions import UserError

from ..models import media_unit


class ReturnMedia(models.TransientModel):
    """ Retrun Media Wizard """
    _name = "return.media"
    _description = "Media Author"

    media_id = fields.Many2one('op.media', 'Media', readonly=True)
    media_unit_id = fields.Many2one(
        'op.media.unit', 'Media Unit', readonly=True, required=True)
    actual_return_date = fields.Date(
        'Actual Return Date', default=lambda self: fields.Date.today(),
        required=True)

    def do_return(self):
        for media in self:
            if media.media_unit_id.state and \
                    media.media_unit_id.state == 'issue':
                media_move_search = self.env['op.media.movement'].search(
                    [('media_unit_id', '=', media.media_unit_id.id),
                     ('state', '=', 'issue')])
                if not media_move_search:
                    raise UserError(_("Can't return media."))
                media_move_search.return_media(media.actual_return_date)
            else:
                raise UserError(_("Media Unit can not be returned \
                because it's state is : %s") % (dict(
                    media_unit.unit_states).get(
                    media.media_unit_id.state)))
