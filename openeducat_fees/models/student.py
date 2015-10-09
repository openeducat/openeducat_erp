# -*- coding: utf-8 -*-
##############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech Receptives(<http://www.techreceptives.com>).
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
##############################################################################

from openerp import models, api


class OpStudent(models.Model):
    _inherit = 'op.student'

    @api.multi
    def action_view_invoice(self):
        '''
        This function returns an action that
        display existing invoices of given student ids and show a invoice"
        '''
        result = self.env.ref('account.action_invoice_tree1')
        id = result and result.id or False
        result = self.env['ir.actions.act_window'].browse(id).read()[0]
        inv_ids = []
        for student in self:
            inv_ids += [invoice.id for invoice in student.invoice_ids]
            result['context'] = {'default_partner_id': student.partner_id.id}
        if len(inv_ids) > 1:
            result['domain'] = \
                "[('id','in',[" + ','.join(map(str, inv_ids)) + "])]"
        else:
            res = self.env.ref('account.invoice_form')
            result['views'] = [(res and res.id or False, 'form')]
            result['res_id'] = inv_ids and inv_ids[0] or False
        return result


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
