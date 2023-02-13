# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenEduCat Inc
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

from odoo import models, fields, api


class OpStudent(models.Model):
    _inherit = "op.student"

    library_card_id = fields.Many2one('op.library.card', 'Library Card')
    media_movement_lines = fields.One2many(
        'op.media.movement', 'student_id', 'Movements')
    media_movement_lines_count = fields.Integer(compute='_compute_media_movement_lines')

    @api.depends('media_movement_lines')
    def _compute_media_movement_lines(self):
        for media in self:
            media.media_movement_lines_count = \
                self.env['op.media.movement'].search_count(
                    [('student_id', '=', self.id)])

    def count_media_movement_lines(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Media Movement',
            'view_mode': 'tree,form',
            'res_model': 'op.media.movement',
            'domain': [('student_id', '=', self.id)],
            'target': 'current',
        }
