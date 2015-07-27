# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
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
###############################################################################

from openerp import models, fields, api


class OpPlacementOffer(models.Model):
    _name = 'op.placement.offer'
    _description = 'Placement Offer'

    name = fields.Char('Company Name', required=True)
    student_id = fields.Many2one('op.student', 'Student Name', required=True)
    join_date = fields.Date('Join Date')
    offer_package = fields.Char('Offered Package', size=256)
    training_period = fields.Char('Training Period', size=256)
    state = fields.Selection(
        [('d', 'Draft'), ('o', 'Offer'), ('j', 'Join'), ('r', 'Rejected'),
         ('c', 'Cancel')], 'State', default='d')

    @api.one
    def placement_offer(self):
        self.state = 'o'

    @api.one
    def placement_join(self):
        self.state = 'j'

    @api.one
    def confirm_rejected(self):
        self.state = 'r'

    @api.one
    def confirm_to_draft(self):
        self.state = 'd'

    @api.one
    def confirm_cancel(self):
        self.state = 'c'


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
