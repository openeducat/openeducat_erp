# -*- coding: utf-8 -*-
##############################################################################
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
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class OpStudentFeesDetails(models.Model):
    _name = "op.student.fees.details"
    _description = "Student Fees Details"
    _rec_name = 'student_id'

    fees_line_id = fields.Many2one('op.fees.terms.line', 'Fees Line')
    invoice_id = fields.Many2one('account.move', 'Invoice ID')
    amount = fields.Monetary('Fees Amount', currency_field='currency_id')
    date = fields.Date('Submit Date')
    product_id = fields.Many2one('product.product', 'Product')
    student_id = fields.Many2one('op.student', 'Student', required=True)
    fees_factor = fields.Float("Fees Factor")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('invoice', 'Invoice Created'),
        ('cancel', 'Cancel')
    ], string='Status', copy=False)
    invoice_state = fields.Selection(related="invoice_id.state",
                                     string='Invoice Status',
                                     readonly=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company)
    after_discount_amount = fields.Monetary(compute="_compute_discount_amount",
                                            currency_field='currency_id',
                                            string='After Discount Amount')
    discount = fields.Float(string='Discount (%)',
                            digits='Discount', default=0.0)

    course_id = fields.Many2one('op.course', 'Course', required=False)
    batch_id = fields.Many2one('op.batch', 'Batch', required=False)

    @api.depends('discount')
    def _compute_discount_amount(self):
        for discount in self:
            discount_amount = discount.amount * discount.discount / 100.0
            discount.after_discount_amount = discount.amount - discount_amount

    @api.depends('company_id')
    def _compute_currency_id(self):
        main_company = self.env['res.company']._get_main_company()
        for template in self:
            template.currency_id = \
                template.company_id.sudo().currency_id.id or main_company.currency_id.id

    currency_id = fields.Many2one(
        'res.currency', string='Currency', compute='_compute_currency_id',
        default=lambda self: self.env.company.currency_id.id)

    def get_invoice(self):
        """ Create invoice for fee payment process of student """
        inv_obj = self.env['account.move']
        partner_id = self.student_id.partner_id
        # student = self.student_id
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
        element_id = self.env['op.fees.element'].search([
            ('fees_terms_line_id', '=', self.fees_line_id.id)])
        invoice_line_list = []
        if element_id:
            for records in element_id:
                invoice_line_list.append((0, 0, {
                    'name': records.product_id.name,
                    'account_id': account_id,
                    'price_unit': records.value * self.amount / 100,
                    'quantity': 1.0,
                    'discount': self.discount or False,
                    'product_uom_id': records.product_id.uom_id.id,
                    'product_id': records.product_id.id,
                }))
        else:
            invoice_line_list.append((0, 0, {
                'name': name,
                'account_id': account_id,
                'price_unit': amount,
                'quantity': 1.0,
                'discount': self.discount or False,
                'product_uom_id': product.uom_id.id,
                'product_id': product.id
            }))
        invoice = inv_obj.create({
            'move_type': 'out_invoice',
            'partner_id': partner_id.id,
            'invoice_line_ids': invoice_line_list,
        })
        invoice._compute_tax_totals()
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
                                      tracking=True)
    fees_details_count = fields.Integer(compute='_compute_fees_details')

    @api.depends('fees_detail_ids')
    def _compute_fees_details(self):
        for fees in self:
            fees.fees_details_count = self.env['op.student.fees.details'].search_count(
                [('student_id', '=', self.id)])

    def count_fees_details(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Fees Details',
            'view_mode': 'tree',
            'res_model': 'op.student.fees.details',
            'context': {'create': False},
            'domain': [('student_id', '=', self.id)],
            'target': 'current',
        }

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
