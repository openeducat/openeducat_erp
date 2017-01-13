# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
##############################################################################


from odoo import models, api


class AccountInvoice(models.Model):

    _inherit = "account.invoice"

    @api.multi
    def action_invoice_paid(self):
        paid_invoice = super(AccountInvoice, self).action_invoice_paid()
        if paid_invoice and self:
            movement = self.env['op.media.movement'].search(
                [('invoice_id', '=', self.id)])
            if movement:
                movement.state = 'return_done'
        return paid_invoice
