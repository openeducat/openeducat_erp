# -*- coding: utf-8 -*-
#/#############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2004-TODAY OpenEduCat Inc(<http://www.OpenEduCat Inc.com>).
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
from osv import osv, fields
from tools.translate import _

class reserve_book(osv.osv_memory):
    """ Reserve Book """

    _name = 'reserve.book'

    _columns = {
        'partner_id': fields.many2one('res.partner', required=True),
    }

    def set_partner(self, cr, uid, ids, context={}):
        value = {}
        book_movement = self.pool.get("op.book.movement")
        partner = self.browse(cr, uid, ids[0]).partner_id
        book_movement.write(cr, uid, context.get('active_ids',False),
                            {'partner_id': partner.id,'reserver_name': partner.name})
        value = {'type': 'ir.actions.act_window_close'}
        return value


reserve_book()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
