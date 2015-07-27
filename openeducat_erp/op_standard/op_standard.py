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


class OpStandard(models.Model):
    _name = 'op.standard'
    _order = 'sequence'

    code = fields.Char('Code', size=8, required=True)
    name = fields.Char('Name', size=32, required=True)
    course_id = fields.Many2one('op.course', 'Course', required=True)
    payment_term = fields.Many2one('account.payment.term', 'Payment Term')
    sequence = fields.Integer('Sequence')
    division_ids = fields.Many2many('op.division', string='Divisions')
    student_ids = fields.Many2many('op.student', string='Student(s)')
#     class_ids = fields.Many2many('op.gr.setup', string='Class')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
