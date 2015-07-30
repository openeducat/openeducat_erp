# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
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


class OpLibraryCardType(models.Model):
    _name = 'op.library.card.type'
    _description = 'Library Card Type'

    name = fields.Char('Name', size=256, required=True)
    duration = fields.Float(
        'Duration', help='Duration in terms of Number of Lead Days',
        required=True)
    penalty_amt_per_day = fields.Float('Penalty Amount Per Day', required=True)


class OpLibraryCard(models.Model):
    _name = 'op.library.card'
    _rec_name = 'number'
    _description = 'Library Card'

    partner_id = fields.Many2one(
        'res.partner', 'Student/Faculty', required=True)
    number = fields.Char('Number', size=256, required=True)
    library_card_type_id = fields.Many2one(
        'op.library.card.type', 'Library Card Type', required=True)
    issue_date = fields.Date('Issue Date', required=True)
    allow_book = fields.Integer(
        'No. Of Book Allow', size=10, required=True)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
