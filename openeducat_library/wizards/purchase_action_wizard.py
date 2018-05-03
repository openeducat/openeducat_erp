# -*- coding: utf-8 -*-

from odoo import models, api, fields


class PurchaseActionWizard(models.TransientModel):
    _name = 'purchase.action.wizard'
    _description = 'Wizard for Purchase Action '

    state = fields.Selection([
        ('request', 'Requested'),
        ('accept', 'Accepted'),
        ('reject', 'Rejected')
    ], 'State', default='request', required=True)

    @api.multi
    def purchase_action(self):
        active_ids = self.env.context['active_ids']
        records = self.env['op.media.purchase'].search(
            [('id', 'in', active_ids)])
        for record in records:
            if self.state == 'request':
                record.act_requested()
            elif self.state == 'accept':
                record.act_accept()
            elif record.state == 'reject':
                record.act_reject()
