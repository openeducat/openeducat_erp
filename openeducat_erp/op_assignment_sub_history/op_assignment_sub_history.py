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

from openerp import models, fields


class OpAssignmentSubHistory(models.Model):
    _name = 'op.assignment.sub.history'

    assign_sub_id = fields.Many2one(
        'op.assignment.sub.line', 'Assignment', required=True)
    description = fields.Text('Description')
    state = fields.Selection([
        ('d', 'Draft'), ('s', 'Submitted'), ('a', 'Accepted'),
        ('r', 'Rejected'), ('c', 'Change Req.')], 'State')
    change_date = fields.Datetime('Submission Date')
    faculty_id = fields.Many2one('op.faculty', 'Faculty', required=True)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
