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


class OpAssignmentSubLine(models.Model):
    _name = 'op.assignment.sub.line'
    _rec_name = 'assignment_id'

    assignment_id = fields.Many2one(
        'op.assignment', 'Assignment', required=True)
    student_id = fields.Many2one('op.student', 'Student', required=True)
    description = fields.Text('Description')
    state = fields.Selection(
        [('d', 'Draft'), ('s', 'Submitted'), ('a', 'Accepted'),
         ('r', 'Rejected'), ('c', 'Change Req.')], 'State', default='d')
    submission_date = fields.Datetime(
        'Submission Date', readonly=True,
        default=lambda self: fields.Datetime.now(), required=True)
    note = fields.Text('Note')
    history_line = fields.One2many(
        'op.assignment.sub.history', 'assign_sub_id', string='Change History')

    @api.one
    def act_draft(self):
        self.state = 'd'

    @api.one
    def act_submit(self):
        self.state = 's'

    @api.one
    def act_accept(self):
        self.state = 'a'

    @api.one
    def act_change_req(self):
        self.state = 'c'

    @api.one
    def act_reject(self):
        self.state = 'r'

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
