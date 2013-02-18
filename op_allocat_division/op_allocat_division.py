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

class op_allocat_division(osv.osv):
    _name = 'op.allocat.division'

    _columns = {
            'name': fields.char(size=128, string='Name'),
            'course_id': fields.many2one('op.course', 'Course'),
            'standard_id': fields.many2one('op.standard', 'Standard'),
            'division_id': fields.many2one('op.division', 'Division'),
            'student_ids': fields.many2many('op.student', 'div_student_rel', 'op_division_id', 'op_student_id', string='Student(s)'),
    }

op_allocat_division()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
