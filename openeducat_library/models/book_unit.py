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

from openerp import models, fields

unit_states = [('available', 'Available'), ('issue', 'Issued'),
               ('reserve', 'Reserved'), ('lost', 'Lost')]


class OpBookUnit(models.Model):
    _name = 'op.book.unit'
    _inherit = 'mail.thread'
    _description = 'Book Unit'

    name = fields.Char('Name', required=True)
    book_id = fields.Many2one(
        'op.book', 'Book', required=True, track_visibility='onchange')
    barcode = fields.Char('Barcode', size=20)
    movement_lines = fields.One2many(
        'op.book.movement', 'book_unit_id', 'Movements')
    state = fields.Selection(
        unit_states, 'State', default='available', track_visibility='onchange')

    _sql_constraints = [
        ('unique_name_barcode',
         'unique(barcode)',
         'Barcode must be unique per book unit!'),
    ]


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
