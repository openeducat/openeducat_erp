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

from openerp import models, api, _
from openerp.exceptions import Warning


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.onchange('user_id')
    def onchange_user(self):
        if self.user_id:
            self.user_id.partner_id.supplier = True
            self.address_home_id = self.user_id.partner_id.id
            self.work_email = self.user_id.email
            self.identification_id = False
            return {'domain':
                    {'address_id': [('id', '=', self.user_id.partner_id.id)]}}

    @api.one
    def check_address(self):
        if self.address_home_id and self.address_id and \
                self.address_home_id != self.address_id:
            raise Warning(_('Configuration Error!'), _(
                'Home Address and Working Address should be same!'))

    @api.onchange('address_id')
    def onchange_address_id(self):
        self.check_address()
        if self.address_id:
            self.work_phone = self.address_id.phone
            self.mobile_phone = self.address_id.mobile

    @api.onchange('address_home_id')
    def onchange_address_home_id(self):
        self.check_address()
        if self.address_home_id:
            self.address_home_id.write({'supplier': True, 'employee': True})
