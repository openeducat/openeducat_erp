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

from openerp import models, fields, tools


class res_company(models.Model):
    _inherit = "res.company"

    signature = fields.Binary('Signature')
    accredetion = fields.Text('Accredetion')
    approval_authority = fields.Text('Approval Authority')


class res_users(models.Model):
    _inherit = "res.users"

    parent_ids = fields.One2many('op.parent', 'user_id', 'Parents')
    user_line = fields.One2many('op.student', 'user_id', 'User Line')

    @tools.ormcache(skiparg=2)
    def has_group(self, cr, uid, group_ext_id, context=None):
        return super(res_users, self).has_group(cr, uid, group_ext_id)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
