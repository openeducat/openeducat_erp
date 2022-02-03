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

from odoo import models, fields


class OpFaculty(models.Model):
    _inherit = "op.faculty"

    session_ids = fields.One2many('op.session', 'faculty_id', 'Sessions')
    session_count = fields.Integer()

    def count_purchase_order(self):
        session = self.env['op.session'].search([('faculty_id', '=', self.id)])
        count = 0
        for rec in session:
            count = count + len(rec)
            self.write({'session_count': count})
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sessions',
            'view_mode': 'tree,form',
            'res_model': 'op.session',
            'domain': [('faculty_id', '=', self.id)],
            'target': 'current',
        }
