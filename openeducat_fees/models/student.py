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

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class OpStudentFeesDetails(models.Model):
    _name = "op.student.fees.details"
    _description = "Student Fees Details"

    fees_line_id = fields.Many2one('op.fees.terms.line', 'Fees Line')
    invoice_id = fields.Many2one('account.move', 'Invoice ID')
    amount = fields.Float('Fees Amount', currency_field='currency_id')
    date = fields.Date('Submit Date')
    product_id = fields.Many2one('product.product', 'Product')
    student_id = fields.Many2one('op.student', 'Student')
    fees_factor = fields.Float("Fees Factor")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('invoice', 'Invoice Created'),
        ('cancel', 'Cancel')
    ], string='Status', copy=False)
    invoice_state = fields.Selection([
        ('draft', 'Draft'), ('proforma', 'Pro-forma'),
        ('proforma2', 'Pro-forma'), ('open', 'Open'),
        ('paid', 'Paid'), ('cancel', 'Cancelled')], 'Invoice',
        related="invoice_id.state", readonly=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.user.company_id)

    @api.depends('company_id')
    def _compute_currency_id(self):
        main_company = self.env['res.company']._get_main_company()
        for template in self:
            template.currency_id = template.company_id.sudo().currency_id.id or main_company.currency_id.id

    currency_id = fields.Many2one('res.currency', string='Currency', compute='_compute_currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)

    def get_invoice(self):
        """ Create invoice for fee payment process of student """
        inv_obj = self.env['account.move']
        partner_id = self.student_id.partner_id
        student = self.student_id
        account_id = False
        product = self.product_id

        if product.property_account_income_id:
            account_id = product.property_account_income_id.id
        if not account_id:
            account_id = product.categ_id.property_account_income_categ_id.id
        if not account_id:
            raise UserError(
                _('There is no income account defined for this product: "%s".'
                  'You may have to install a chart of account from Accounting'
                  ' app, settings menu.') % product.name)
        if self.amount <= 0.00:
            raise UserError(
                _('The value of the deposit amount must be positive.'))
        else:
            amount = self.amount
            name = product.name

        invoice = inv_obj.create({
            'partner_id': student.name,
            'type': 'out_invoice',
            'partner_id': partner_id.id,

        })
        element_id = self.env['op.fees.element'].search([
            ('fees_terms_line_id', '=', self.fees_line_id.id)])
        for records in element_id:

            if records:
                line_values = {'name': records.product_id.name,
                               'account_id': account_id,
                               'price_unit': records.value * self.amount / 100,
                               'quantity': 1.0,
                               'discount': 0.0,
                               'product_uom_id': records.product_id.uom_id.id,
                               'product_id': records.product_id.id, }
                invoice.write({'invoice_line_ids': [(0, 0, line_values)]})

        if not element_id:
            line_values = {'name': name,
                           # 'origin': student.gr_no,
                           'account_id': account_id,
                           'price_unit': amount,
                           'quantity': 1.0,
                           'discount': 0.0,
                           'product_uom_id': product.uom_id.id,
                           'product_id': product.id}
            invoice.write({'invoice_line_ids': [(0, 0, line_values)]})

        invoice._compute_invoice_taxes_by_group()
        self.state = 'invoice'
        self.invoice_id = invoice.id
        return True

    def action_get_invoice(self):
        value = True
        if self.invoice_id:
            form_view = self.env.ref('account.view_move_form')
            tree_view = self.env.ref('account.view_invoice_tree')
            value = {
                'domain': str([('id', '=', self.invoice_id.id)]),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'account.move',
                'view_id': False,
                'views': [(form_view and form_view.id or False, 'form'),
                          (tree_view and tree_view.id or False, 'tree')],
                'type': 'ir.actions.act_window',
                'res_id': self.invoice_id.id,
                'target': 'current',
                'nodestroy': True
            }
        return value


class OpStudent(models.Model):
    _inherit = "op.student"

    fees_detail_ids = fields.One2many('op.student.fees.details',
                                      'student_id',
                                      string='Fees Collection Details',
                                      track_visibility='onchange')

    def action_view_invoice(self):
        '''
        This function returns an action that
        display existing invoices of given student ids and show a invoice"
        '''
        result = self.env.ref('account.action_move_out_invoice_type')
        fees = result and result.id or False
        result = self.env['ir.actions.act_window'].browse(fees).read()[0]
        inv_ids = []
        for student in self:
            inv_ids += [invoice.id for invoice in student.invoice_ids]
            result['context'] = {'default_partner_id': student.partner_id.id}
        if len(inv_ids) > 1:
            result['domain'] = \
                "[('id','in',[" + ','.join(map(str, inv_ids)) + "])]"
        else:
            res = self.env.ref('account.view_move_form')
            result['views'] = [(res and res.id or False, 'form')]
            result['res_id'] = inv_ids and inv_ids[0] or False
        return result
