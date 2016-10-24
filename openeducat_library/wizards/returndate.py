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

from openerp import models, fields, api


class ReturnDate(models.TransientModel):

    """ Assign return date """
    _name = 'return.date'

    actual_return_date = fields.Date(
        'Actual Return Date', required=True,
        default=lambda self: fields.Date.today())

    @api.one
    def assign_return_date(self):
        media_movement = self.env['op.media.movement'].browse(
            self.env.context.get('active_ids', False))
        media_movement.write(
            {'actual_return_date': self.actual_return_date})
        media_movement.calculate_penalty()
        if media_movement.penalty > 0.0:
            media_movement.create_penalty_invoice()
            media_movement.state = 'return'
        else:
            media_movement.state = 'return_done'
        media_movement.media_unit_id.state = 'available'
