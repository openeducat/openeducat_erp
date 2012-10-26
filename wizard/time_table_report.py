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
from osv import osv
from osv import fields
import datetime
from openerp.addons.openeducat_erp import utils
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
        'standard_id': fields.many2one('op.standard', 'Standard', required=True),
        'division_id': fields.many2one('op.division', 'Division',  required=True),
        'start_date':fields.date('Start Date', required=True),
        'end_date':fields.date('End Date', required=True),
    }

    def gen_time_table_report(self, cr, uid, ids, context={}):
        value = {}
        data = self.read(cr, uid, ids, ['standard_id','division_id','start_date', 'end_date'], context=context)

        time_table_ids = self.pool.get('op.timetable').search(cr, uid, [('standard_id','=',data[0]['standard_id'][0]),
                                                                        ('division_id','=',data[0]['division_id'][0]),
                                                                        ('start_datetime','>',data[0]['start_date'] + '%H:%M:%S'),
                                                                        ('end_datetime','<',data[0]['end_date'] + '%H:%M:%S'),
                                                                        ],order='start_datetime asc')

        data[0].update({'time_table_ids': time_table_ids})

        value = {
                'type': 'ir.actions.report.xml',
                'report_name': 'time.table.report',
                'datas': data[0],
                }
        return value

time_table_report()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
