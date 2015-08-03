# -*- coding: utf-8 -*-
##############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech Receptives(<http://www.techreceptives.com>).
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

from openerp import models, fields, api


class OpStudent(models.Model):
    _inherit = 'op.student'

    invoice_exists = fields.Boolean('Invoice')

    @api.multi
    def create_invoice(self):
        """ Create invoice for fee payment process of student """

        invoice_pool = self.env['account.invoice']

        default_fields = invoice_pool.fields_get(self)
        invoice_default = invoice_pool.default_get(default_fields)

        for student in self:
            type = 'out_invoice'
            partner_id = student.partner_id.id
            onchange_partner = invoice_pool.onchange_partner_id(
                type, partner_id)
            invoice_default.update(onchange_partner['value'])

            invoice_data = {
                'partner_id': student.partner_id.id,
                'date_invoice': fields.Date.today(),
                'payment_term': student.course_id.payment_term and
                student.course_id.payment_term.id or False,
            }

        invoice_default.update(invoice_data)
        invoice_id = invoice_pool.create(invoice_default).id
        self.write({'invoice_ids': [(4, invoice_id)], 'invoice_exists': True})
        form_view = self.env.ref('account.invoice_form')
        tree_view = self.env.ref('account.invoice_tree')
        value = {
            'domain': str([('id', '=', invoice_id)]),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.invoice',
            'view_id': False,
            'views': [(form_view and form_view.id or False, 'form'),
                      (tree_view and tree_view.id or False, 'tree')],
            'type': 'ir.actions.act_window',
            'res_id': invoice_id,
            'target': 'current',
            'nodestroy': True
        }
        return value

    @api.multi
    def action_view_invoice(self):
        '''
        This function returns an action that
        display existing invoices of given student ids and show a invoice"
        '''
        result = self.env.ref('account.action_invoice_tree1')
        id = result and result.id or False
        result = self.env['ir.actions.act_window'].browse(id).read()[0]
        # compute the number of invoices to display
        inv_ids = []
        for so in self:
            inv_ids += [invoice.id for invoice in so.invoice_ids]
        # choose the view_mode accordingly
        if len(inv_ids) > 1:
            result['domain'] = \
                "[('id','in',[" + ','.join(map(str, inv_ids)) + "])]"
        else:
            res = self.env.ref('account.invoice_form')
            result['views'] = [(res and res.id or False, 'form')]
            result['res_id'] = inv_ids and inv_ids[0] or False
        return result


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
