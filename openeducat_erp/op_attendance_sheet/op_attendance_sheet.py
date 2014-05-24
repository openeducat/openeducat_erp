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

class op_attendance_sheet(osv.osv):
    _name = 'op.attendance.sheet'

    def _total_present(self, cr, uid, ids, name, arg, context=None):
        res = {}

        for sheet in self.browse(cr, uid, ids, context):
            present_cnt = 0
            for line in sheet.attendance_line:

                if line.present == True:
                    present_cnt =  present_cnt + 1
            res[sheet.id] = present_cnt
        return res

    def _total_absent(self, cr, uid, ids, name, arg, context=None):
        res = {}

        for sheet in self.browse(cr, uid, ids, context):
            absent_cnt = 0
            for line in sheet.attendance_line:
                if line.present == False:
                    absent_cnt =  absent_cnt + 1
            res[sheet.id] = absent_cnt
        return res

    _columns = {
            'name': fields.char(size=8, string='Name'),    
            'register_id': fields.many2one('op.attendance.register', string='Register', required=True),
            'attendance_date': fields.date(string='Date', required=True),
            'attendance_line': fields.one2many('op.attendance.line', 'attendance_id', string='Attendance Line', required=True),
            'total_present': fields.function(_total_present, string='Total Present', type='integer',method=True),
            'total_absent': fields.function(_total_absent, string='Total Absent', type='integer',method=True),
            'teacher_id': fields.many2one('op.faculty', string='Teacher'),
    }

op_attendance_sheet()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
