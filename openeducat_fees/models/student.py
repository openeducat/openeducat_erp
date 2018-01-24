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

from odoo import models, api, fields, exceptions, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging

_logger = logging.getLogger(__name__)


class OpStudentFeesDetails(models.Model):
    _name = 'op.student.fees.details'
    _description = 'Student Fees Details'

    student_id = fields.Many2one('op.student', 'Student')
    reference = fields.Reference(string='Origin', selection='_get_document_types')
    fees_line_id = fields.Many2one('op.fees.terms.line', 'Fees Line')
    invoice_id = fields.Many2one('account.invoice', 'Invoice')
    amount = fields.Float('Fees Amount')
    date = fields.Date('Submit Date')
    product_id = fields.Many2one('product.product', 'Product')
    state = fields.Selection([
        ('draft', 'Draft'), ('invoice', 'Invoice Created')], 'Status', default='draft')
    invoice_state = fields.Selection([
        ('draft', 'Draft'), ('proforma', 'Pro-forma'),
        ('proforma2', 'Pro-forma'), ('open', 'Open'),
        ('paid', 'Paid'), ('cancel', 'Cancelled')], 'State',
        related="invoice_id.state", readonly=True)


    @api.model
    def _get_document_types(self):
        records = self.env['ir.model'].search([('model', '=', 'op.batch')])
        return [(record.model, record.name) for record in records] + [('', '')]
    
    
    @api.multi
    def get_invoice(self):
        """ Create invoice for fee payment process of student """

        inv_obj = self.env['account.invoice']
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
                _('There is no income account defined for this product: "%s". \
                   You may have to install a chart of account from Accounting \
                   app, settings menu.') % (product.name,))

        if self.amount <= 0.00:
            raise UserError(_('The value of the deposit amount must be \
                             positive.'))
        else:
            amount = self.amount
            name = product.name

        invoice = inv_obj.create({
            'name': student.name,
            'origin': student.gr_no or False,
            'type': 'out_invoice',
            'reference': False,
            'account_id': partner_id.property_account_receivable_id.id,
            'partner_id': partner_id.id,
            'date_invoice': self.date,
            'invoice_line_ids': [(0, 0, {
                'name': name,
                'origin': student.gr_no,
                'account_id': account_id,
                'price_unit': amount,
                'quantity': 1.0,
                'discount': 0.0,
                'uom_id': product.uom_id.id,
                'product_id': product.id,
            })],
        })
        invoice.compute_taxes()
        self.state = 'invoice'
        self.invoice_id = invoice.id
        return True


    def action_get_invoice(self):
        value = True
        if self.invoice_id:
            form_view = self.env.ref('account.invoice_form')
            tree_view = self.env.ref('account.invoice_tree')
            value = {
                'domain': str([('id', '=', self.invoice_id.id)]),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'account.invoice',
                'view_id': False,
                'views': [(form_view and form_view.id or False, 'form'),
                          (tree_view and tree_view.id or False, 'tree')],
                'type': 'ir.actions.act_window',
                'res_id': self.invoice_id.id,
                'target': 'current',
                'nodestroy': True
            }
        return value
        
class OpStudentCourse(models.Model):
    _inherit = 'op.student.course'
    
    
    def create_reference(self):
        return 'op.student.course,'+str(self.id)
    
    
    def check_fee_exist(self, term_line):
        model = self.env['op.student.fees.details']
        
        fees = model.search([('student_id', '=', self.student_id.id),\
                             ('reference', '=', self.create_reference()),\
                             ('product_id', '=', self.course_id.product_id.id),\
                             ('fees_line_id', '=', term_line.id)])
        
        return len(fees) > 0
    

    def generate_fees(self):
        count = 0
        if self.course_id.fees_term_id and self.course_id.product_id:
            for term_line in self.course_id.fees_term_id.line_ids:
                if not self.check_fee_exist(term_line):
                    record = {}
                    record['student_id'] = self.student_id.id
                    record['reference'] = self.create_reference()
                    record['fees_line_id'] = term_line.id
                    record['amount'] = self.course_id.product_id.list_price * term_line.value / 100.00
                    months = int(round(term_line.due_days / 30))
                    days = int(round(term_line.due_days % 30))
                    record['date'] = (fields.Date.from_string(self.batch_id.start_date) + relativedelta(months=months, days=days))
                    record['product_id'] = self.course_id.product_id.id
                    record['state'] = 'draft'
                    val = [[0, False, record]]
                    self.student_id.write({'fees_detail_ids': val})
                    count+=1
        return count


        
class OpStudent(models.Model):
    _inherit = 'op.student'
    
    
    fees_detail_ids = fields.One2many('op.student.fees.details', 'student_id',
                                      'Fees Collection Details')
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

    @api.multi
    def generate_fees(self):
        count=0
        for record in self:
            for course in record.course_detail_ids:
                count = count + course.generate_fees()
        
        if count > 0:
            text = _('Fees generation finished with ') +str(count) + _('fees created')
        else:
            text = _('Fees generation finished with none fee created')
        
        _logger.info(text)
