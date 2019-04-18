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

from odoo import models, api


class ReportFeesAnalysis(models.AbstractModel):
    _name = 'report.openeducat_fees.report_fees_analysis'

    def get_invoice_amount(self, student_id):
        total_amount = 0.0
        paid_amount = 0.0
        for inv in self.env['account.invoice'].search([
            ('partner_id', '=', student_id.partner_id.id),
            ('state', 'in', ['open', 'paid']),
        ]):
            total_amount += inv.amount_total
            paid_amount += inv.amount_total - inv.residual
        return [total_amount, paid_amount]

    @api.model
    def get_report_values(self, docids, data=None):
        student_ids = []
        if data['fees_filter'] == 'student':
            student_ids = self.env['op.student'].browse([data['student']])
        else:
            student_ids = self.env['op.student'].search(
                [('course_detail_ids.course_id', '=', data['course'])])
        docargs = {
            'doc_ids': self.ids,
            'doc_model': 'op.student',
            'docs': student_ids,
            'get_invoice_amount': self.get_invoice_amount,
        }
        return docargs
