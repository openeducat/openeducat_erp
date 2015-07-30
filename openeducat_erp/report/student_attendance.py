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

import time

from openerp.osv import osv
from openerp.report import report_sxw


class StudentAttendance(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        super(StudentAttendance, self).__init__(
            cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_date': self.get_date,
            'get_data': self.get_data
        })

    def get_date(self, data):
        dt_from = data['from_date']
        dt_to = data['to_date']
        from_to = 'From : ' + dt_from + ' ' + 'To : ' + ' ' + dt_to
        return from_to

    def get_data(self, data):

        if data['from_date'].split()[0] > data['to_date'].split()[0]:
            raise osv.except_osv(
                ('Error!'), ("From Date is not greater than To Date "))
        else:
            student_pool = self.pool.get('op.student')
            sheet_pool = self.pool.get('op.attendance.sheet')

            student = student_pool.browse(
                self.cr, self.uid, data['student_id'])
            sheet_search = sheet_pool.search(
                self.cr, self.uid,
                [('attendance_date', '>=', data['from_date']),
                 ('attendance_date', '<=', data['to_date'])])

            lst = []
            for sheet in sheet_search:
                sheet_browse = sheet_pool.browse(self.cr, self.uid, sheet)
                for line in sheet_browse.attendance_line:
                    dic = {}
                    if data['student_id'] == line.student_id.id and \
                            not line.present:
                        dic = {
                            'absent_date': sheet_browse.attendance_date,
                            'remark': line.remark
                        }
                        lst.append(dic)
            return [{'total': len(lst),
                     'line': lst,
                     'student_id': student.name}]

report_sxw.report_sxw(
    'report.student.attendance', 'op.student',
    'addons/openeducat_erp/report/student_attendance_report.rml',
    parser=StudentAttendance, header='external')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
