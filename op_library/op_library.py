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

from osv import osv
from osv import fields

class op_library_card_type(osv.osv):
    _name = 'op.library.card.type'
    _description = 'Library Card Type'

    _columns = {
        'name':fields.char('Name',size=256),
        'duration': fields.float('Duration'),
        'penalty_amt_per_day': fields.float('Penalty Amount Per Day'),
    }

op_library_card_type()

class op_library_card(osv.osv):
    _name = 'op.library.card'
    _description = 'Library Card'

    _columns = {
        'partner_id':fields.many2one('res.partner','Partner'),
        'name':fields.char('Number',size=256),
        'library_card_type_id': fields.many2one('op.library.card.type', 'Library Card Type'),
                'issue_date':fields.date('Issue Date')
    }

op_library_card()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
