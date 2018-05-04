# -*- coding: utf-8 -*-

from datetime import date

from odoo import models, api, fields


class MediaIssueReturnAction(models.TransientModel):
    _name = 'media.issue.return'
    _description = 'Wizard for Issue/Return Media'
    state = fields.Selection([
        ('issue', 'Issue Media'),
        ('return', 'Return Media'),
        ('return_invoice', 'Return with invoice')
    ], 'Status',
        default='issue', required=True)

    @api.multi
    def issue_return_media(self):
        active_ids = self.env.context['active_ids']
        records = self.env['op.media.movement'].search(
            [('id', 'in', active_ids)])
        for record in records:
            if self.state == 'issue':
                record.issue_media()
            elif self.state in ('return', 'return_invoice') \
                    and record.state == 'issue':
                wiz = self.env['return.media'].create({
                    'media_id': record.media_id.id,
                    'media_unit_id': record.media_unit_id.id,
                    'actual_return_date': date.today()
                })
                wiz.do_return()
            if self.state == 'return_invoice' and record.state == 'return':
                record.create_penalty_invoice()
