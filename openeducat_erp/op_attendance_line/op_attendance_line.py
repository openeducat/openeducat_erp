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
from openerp.osv import osv, fields

class op_attendance_line(osv.osv):
    _name = 'op.attendance.line'
    _rec_name = 'attendance_id'

    _columns = {
            'attendance_id': fields.many2one('op.attendance.sheet', string='Attendance', required=True),
            'student_id': fields.many2one('op.student', string='Student', required=True),
            'present': fields.boolean(string='Present ?'),
            'course_id':fields.related('student_id', 'course_id',type='many2one',relation='op.course',string='Course',store=True, readonly=True),
            'standard_id': fields.related('student_id', 'standard_id', type='many2one', relation='op.standard', string='Standard', store=True, readonly=True),
            'division_id': fields.related('student_id', 'division_id', type='many2one', relation='op.division', string='Division', store=True, readonly=True),
            'remark': fields.char(size=256, string="Remark"),
            'attendance_date':fields.related('attendance_id','attendance_date',type='date',relation='op.attendance.sheet', string='Date', store=True, readonly=True)
    }
    
    def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
        print "__op_attendance_line_____read_____ids____",ids
        print "__op_attendance_line_____read_____fields____",fields
        return super(op_attendance_line, self).read(cr, uid, ids, fields=fields, context=context, load=load)

op_attendance_line()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
