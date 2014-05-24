# -*- coding: utf-8 -*-
#/#############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2004-TODAY Tech-Receptives(<http://www.tech-receptives.com>).
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
#/#############################################################################

from openerp.osv import osv,fields

class op_library_card_type(osv.osv):
    _name = 'op.library.card.type'
    _description = 'Library Card Type'

    _columns = {
        'name':fields.char('Name',size=256, required=True),
        'duration': fields.float('Duration',help="Duration in terms of Number of Lead Days", required=True),
        'penalty_amt_per_day': fields.float('Penalty Amount Per Day', required=True),
    }

op_library_card_type()

class op_library_card(osv.osv):
    _name = 'op.library.card'
    _rec_name = 'number'
    _description = 'Library Card'

    _columns = {
        'partner_id':fields.many2one('res.partner','Student/Faculty', required=True),
        'number':fields.char('Number',size=256, required=True),
        'library_card_type_id': fields.many2one('op.library.card.type', 'Library Card Type', required=True),
        'issue_date':fields.date('Issue Date', required=True),
        'allow_book': fields.integer(string="No. Of Book Allow", size=10, required=True),
    }

op_library_card()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
