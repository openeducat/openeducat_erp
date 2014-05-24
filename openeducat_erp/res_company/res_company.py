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
from openerp.osv import osv, fields

class res_company(osv.osv):
    _inherit = "res.company"
    _columns = {
                'signature': fields.binary('Signature'),
                'accredetion': fields.text('Accredetion'),
                'approval_authority': fields.text('Approval Authority'),
                }
res_company()

class res_users(osv.osv):
    _inherit = "res.users"
    _columns = {
                'parent_ids':fields.one2many('op.parent','user_id','Parents'),
                'user_line': fields.one2many('op.student', 'user_id', 'User Line')
                }
res_users()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
