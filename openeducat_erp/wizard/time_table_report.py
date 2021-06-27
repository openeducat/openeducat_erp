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
from osv import osv
from osv import fields
import datetime
import time
week_number  = {
    'Mon': 1,
    'Tue': 2,
    'Web': 3,
    'Thu': 4,
    'Fri': 5,
    'Sat': 6,
    'Sun': 7,
}

class time_table_report(osv.osv_memory):
    _name = 'time.table.report'
    _description = 'Generate Time Table Report'
    _columns = {
        'standard_id': fields.many2one('op.standard', 'Standard'),
        'division_id': fields.many2one('op.division', 'Division'),
        'faculty_id': fields.many2one('op.faculty', string='Faculty'),
        'start_date':fields.date('Start Date', required=True),
        'end_date':fields.date('End Date', required=True),
        'state': fields.selection([('s','Student'),('t','Teacher')],string='Select',\
                                  required=True),
    }

    _defaults = {
                 'state': 't',
                 'start_date': time.strftime('2012-10-01'),
                 'end_date': time.strftime('2012-10-31')
                 }

    def gen_time_table_report(self, cr, uid, ids, context={}):
        value = {}
        data = self.read(cr, uid, ids, ['start_date', 'end_date','standard_id',\
                            'division_id','state','faculty_id'], context=context)

        if data[0]['state'] == 's':
            time_table_ids = self.pool.get('op.timetable').search(cr, uid, \
                      [('standard_id','=',data[0]['standard_id'][0]),
                        ('division_id','=',data[0]['division_id'][0]),
                        ('start_datetime','>',data[0]['start_date'] + '%H:%M:%S'),
                        ('end_datetime','<',data[0]['end_date'] + '%H:%M:%S'),
                        ],order='start_datetime asc')
            
            data[0].update({'time_table_ids': time_table_ids})
        else:
            teacher_time_table_ids = self.pool.get('op.timetable').search(cr, uid,\
                      [('start_datetime','>',data[0]['start_date'] + '%H:%M:%S'),
                        ('end_datetime','<',data[0]['end_date'] + '%H:%M:%S'),
                        ('faculty_id','=',data[0]['faculty_id'][1]),
                        ],order='start_datetime asc')
        
        
            data[0].update({'teacher_time_table_ids': teacher_time_table_ids})
        
        if data[0]['state'] == 's' :
            value = {
                    'type': 'ir.actions.report.xml',
                    'report_name': 'time.table.report',
                    'datas': data[0],
                    }
            return value
        elif data[0]['state'] == 't':
            value = {
                    'type': 'ir.actions.report.xml',
                    'report_name': 'time.table.teacher.report',
                    'datas': data[0],
                    }
            return value

time_table_report()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
