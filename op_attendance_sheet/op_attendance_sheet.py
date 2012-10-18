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

class op_attendance_sheet(osv.osv):
    _name = 'op.attendance.sheet'
    
    _columns = {
            'register_id': fields.many2one('op.attendance.register', string='Register', required=True),
            'date': fields.date(string='Date', required=True),
            'attendance_line': fields.one2many('op.attendance.line', 'attendance_id', string='Attendance Line', required=True),
            'total_present': fields.integer(string='Total Present', required=True),
            'total_absent': fields.integer(string='Total Absent', required=True),
            'faculty_id': fields.many2one('op.faculty', string='Faculty'),
            'name': fields.char(size=8, string='Name'),
    }
    
    def write(self, cr, uid, ids, vals, context=None):
        for sheet in self.browse(cr, uid, ids, context):
            absent_cnt = 0
            present_cnt = 0
            for line in sheet.attendance_line and sheet.attendance_line:
                if line.present == True: 
                    present_cnt =  present_cnt + 1
                else:
                    absent_cnt =  absent_cnt + 1
            print "BBBBBBBBBBBBBBBBBB*****************",present_cnt,absent_cnt,sheet
        data = {
                'total_present': present_cnt,
                'total_absent':absent_cnt
                }
        vals.update(data)
        print "VVVVVVVVVVVVVVVVVVVVVVVVVV",vals
        return super(op_attendance_sheet, self).write(cr, uid, ids, vals, context=context)
    
op_attendance_sheet()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
