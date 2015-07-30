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


class ResCompany(models.Model):
    _inherit = "res.company"

    signature = fields.Binary('Signature')
    accredetion = fields.Text('Accredetion')
    approval_authority = fields.Text('Approval Authority')


class ResUsers(models.Model):
    _inherit = "res.users"

    parent_ids = fields.One2many('op.parent', 'user_id', 'Parents')
    user_line = fields.One2many('op.student', 'user_id', 'User Line')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
