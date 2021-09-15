# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
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


from odoo import models


class AccountInvoice(models.Model):
    _inherit = "account.move"

    def action_invoice_paid(self):
        paid_invoice = super(AccountInvoice, self).action_invoice_paid()
        if self:
            for record in self:
                movement = self.env['op.media.movement'].sudo().search(
                    [('invoice_id', '=', record.id)])
                if movement and movement.invoice_id.state == 'paid':
                    movement.state = 'return_done'
        return paid_invoice
