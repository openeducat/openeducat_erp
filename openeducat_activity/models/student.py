# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<https://www.openeducat.org>).
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

from odoo import models, fields


class OpStudent(models.Model):
    _inherit = "op.student"

    activity_log = fields.One2many('op.activity', 'student_id',
                                   string='Activity Log')
    activity_count = fields.Integer(compute='compute_count')

    def get_activity(self):
        action = self.env.ref('openeducat_activity.'
                              'act_open_op_activity_view').read()[0]
        action['domain'] = [('student_id', 'in', self.ids)]
        return action

    def compute_count(self):
        for record in self:
            record.activity_count = self.env['op.activity'].search_count(
                [('student_id', 'in', self.ids)])
