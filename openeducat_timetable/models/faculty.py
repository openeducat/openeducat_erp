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

from odoo import models, fields, api


class OpFaculty(models.Model):
    _inherit = "op.faculty"

    session_ids = fields.One2many('op.session', 'faculty_id', 'Sessions')
    session_count = fields.Integer(compute='_compute_session_details')

    @api.depends('session_ids')
    def _compute_session_details(self):
        for session in self:
            session.session_count = self.env['op.session'].search_count(
                [('faculty_id', '=', self.id)])

    def count_sessions_details(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sessions',
            'view_mode': 'list,form',
            'res_model': 'op.session',
            'domain': [('faculty_id', '=', self.id)],
            'target': 'current',
        }
