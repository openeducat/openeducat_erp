# -*- coding: utf-8 -*-
#/#############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2004-TODAY OpenEduCat Inc(<http://www.OpenEduCat Inc.com>).
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

class op_attendance_register(osv.osv):
    _name = 'op.attendance.register'

    _columns = {
            'name': fields.char(size=16, string='Name', required=True),
            'code': fields.char(size=8, string='Code', required=True),
            'course_id': fields.many2one('op.course', string='Course', required=True),
            'batch_id': fields.many2one('op.batch', string='Batch', required=True),
            'standard_id': fields.many2one('op.standard', string='Standard', required=True),
            'division_id': fields.many2one('op.division', string='Division', required=True),
            'subject_id': fields.many2one('op.subject', string='Subject'),
    }

op_attendance_register()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
