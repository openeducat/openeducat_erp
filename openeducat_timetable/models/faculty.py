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

from odoo import api, fields, models


class OpFaculty(models.Model):
    _inherit = "op.faculty"

    session_ids = fields.One2many('op.session', 'faculty_id', 'Sessions')
    session_count = fields.Integer(compute='_compute_session_details')

    @api.depends('session_ids')
    def _compute_session_details(self):
        # Previously `self.id` was used inside the per-record loop —
        # `self` here is the ENTIRE recordset, not the current record,
        # so every faculty row got the count for the first faculty's
        # id (or crashed with "singleton expected" on a multi-record
        # recompute). Use `faculty.id` from the loop variable.
        for faculty in self:
            faculty.session_count = len(faculty.session_ids)

    def count_sessions_details(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sessions',
            'view_mode': 'list,form',
            'res_model': 'op.session',
            'domain': [('faculty_id', '=', self.id)],
            'target': 'current',
        }
