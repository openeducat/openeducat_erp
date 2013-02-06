# -*- coding: utf-8 -*-
#/#############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2004-TODAY Tech-Receptives(<http://www.tech-receptives.com>).
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
#/#############################################################################
from osv import osv, fields

class op_standard(osv.osv):
    _name = 'op.standard'
    _order = 'sequence'

    _columns = {
            'code': fields.char(size=8, string='Code', required=True),
            'name': fields.char(size=32, string='Name', required=True),
            'course_id': fields.many2one('op.course', string='Course', required=True),
            'payment_term': fields.many2one('account.payment.term', 'Payment Term'),
            'sequence':fields.integer('Sequence'),
            'division_ids': fields.many2many('op.division', 'standard_division_rel', 'standard_id', 'division_id', 'Divisions', ),
            'student_ids': fields.many2many('op.student', 'op_student_standard_rel', 'op_student_id', 'op_standard_id', string='Student(s)'),
#            'class_ids': fields.many2many('op.gr.setup', 'op_class_setup_rel','op_standard_id', 'op_setup_id' , string='Class'),
    }

op_standard()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
