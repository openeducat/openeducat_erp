# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
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


class OpCourse(models.Model):
    _name = 'op.course'

    name = fields.Char('Name', size=32, required=True)
    code = fields.Char('Code', size=8, required=True)
    section = fields.Char('Section', size=32, required=True)
    evaluation_type = fields.Selection(
        [('normal', 'Normal'), ('GPA', 'GPA'), ('CWA', 'CWA'), ('CCE', 'CCE')],
        'Evaluation Type', required=True)
    payment_term = fields.Many2one('account.payment.term', 'Payment Term')
    subject_ids = fields.Many2many('op.subject', string='Subject(s)')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
