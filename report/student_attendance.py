# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
##############################################################################

import time
import datetime
from osv import osv, fields
from report import report_sxw



class student_attendance(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(student_attendance, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_data': self.get_data
        })
    
    def get_data(self, data):
        
        student_pool = self.pool.get('op.student')
        sheet_pool = self.pool.get('op.attendance.sheet')

        student = student_pool.browse(self.cr, self.uid, data['student_id'])
        sheet_search = sheet_pool.search(self.cr, self.uid, [('attendance_date','>=', data['from_date']),
                                                      ('attendance_date','<=',data['to_date'])] )
        
        lst = []
        for sheet in sheet_search:
            sheet_browse = sheet_pool.browse(self.cr, self.uid, sheet)
            for line in sheet_browse.attendance_line:
                dic = {}
                if data['student_id'] == line.student_id.id and line.present == False:
                    dic = {
                           'absent_date': sheet_browse.attendance_date,
                           }
                    lst.append(dic)
        return [{'total': len(lst),'line': lst, 'student_id': student.name}]

report_sxw.report_sxw('report.student.attendance','op.student',
                      'addons/openeducat_erp/report/student_attendance_report.rml', 
                      parser=student_attendance, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: