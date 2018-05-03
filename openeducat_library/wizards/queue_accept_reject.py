# -*- coding: utf-8 -*-

from odoo import models, api, fields


class QueueAcceptReject(models.TransientModel):
    _name = 'queue.accept.reject'
    _description = 'Wizard for Accept/Reject Queue'

    state = fields.Selection([
        ('accept', 'Accepted'),
        ('reject', 'Rejected')
    ], 'Status', default='accept', required=True)

    @api.multi
    def accept_reject_queue(self):
        active_ids = self.env.context['active_ids']
        records = self.env['op.media.queue'].search([('id', 'in', active_ids)])
        for record in records:
            if self.state == 'accept':
                record.do_accept()
            else:
                if record.state != 'reject':
                    record.do_reject()
