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
from openerp.osv import osv,fields

import datetime
from openerp.addons.openeducat_erp import utils
import pytz

week_number  = {
    'Mon': 1,
    'Tue': 2,
    'Wed': 3,
    'Thu': 4,
    'Fri': 5,
    'Sat': 6,
    'Sun': 7,
}

class generate_time_table(osv.osv_memory):
    _name = 'generate.time.table'
    _description = 'Generate Time Table'
    _rec_name = 'standard_id'

    _columns = {
        'course_id': fields.many2one('op.course', 'Course', required=True),
        'standard_id': fields.many2one('op.standard', 'Standard', required=True),
        'division_id': fields.many2one('op.division', 'Division',  required=True),
        'time_table_lines':fields.one2many('gen.time.table.line','gen_time_table','Time Table Lines', required=True),
        'time_table_lines_1':fields.one2many('gen.time.table.line','gen_time_table','Time Table Lines', domain=[('day', '=', '1')], required=True),
        'time_table_lines_2':fields.one2many('gen.time.table.line','gen_time_table','Time Table Lines', domain=[('day', '=', '2')], required=True),
        'time_table_lines_3':fields.one2many('gen.time.table.line','gen_time_table','Time Table Lines', domain=[('day', '=', '3')], required=True),
        'time_table_lines_4':fields.one2many('gen.time.table.line','gen_time_table','Time Table Lines', domain=[('day', '=', '4')], required=True),
        'time_table_lines_5':fields.one2many('gen.time.table.line','gen_time_table','Time Table Lines', domain=[('day', '=', '5')], required=True),
        'time_table_lines_6':fields.one2many('gen.time.table.line','gen_time_table','Time Table Lines', domain=[('day', '=', '6')], required=True),
        'start_date':fields.date('Start Date', required=True),
        'end_date':fields.date('End Date', required=True),
    }
    def gen_datewise(self, cr, uid, line, st_date ,en_date, self_obj, context={}):
        time_pool = self.pool.get('op.timetable')
        day_cnt = 7
        curr_date = st_date
        while curr_date <= en_date:
            hour = line.period_id.hour
            if line.period_id.am_pm == 'pm' and int(hour) != 12:
                hour = int(hour)+12
            per_time = '%s:%s:00'%(hour,line.period_id.minute)
            user = self.pool.get('res.users').browse(cr, uid, uid)
            local = pytz.timezone (user.partner_id.tz or 'GMT')
            naive = datetime.datetime.strptime (curr_date.strftime("%Y-%m-%d ") +per_time,"%Y-%m-%d %H:%M:%S")
            local_dt = local.localize(naive, is_dst=None)
            utc_dt = local_dt.astimezone (pytz.utc)
            utc_dt = utc_dt.strftime("%Y-%m-%d %H:%M:%S")
            curr_date = datetime.datetime.strptime(utc_dt, "%Y-%m-%d %H:%M:%S")
            end_time = datetime.timedelta(hours=line.period_id.duration)
            cu_en_date = curr_date + end_time
            a = time_pool.create(cr, uid, {
                        'faculty_id':line.faculty_id.id,
                        'subject_id':line.subject_id.id,
                        'course_id':self_obj.course_id.id,
                        'standard_id':self_obj.standard_id.id,
                        'period_id':line.period_id.id,
                        'division_id':self_obj.division_id.id,
                        'start_datetime':curr_date.strftime("%Y-%m-%d %H:%M:%S"),
                        'end_datetime':cu_en_date.strftime("%Y-%m-%d %H:%M:%S"),
                        'type': curr_date.strftime('%A'),
                        })

            curr_date = curr_date+ datetime.timedelta(days=day_cnt)

        return True
    def act_gen_time_table(self, cr, uid, ids, context={}):
        for self_obj in self.browse(cr, uid, ids, context=context):
            st_date = datetime.datetime.strptime(self_obj.start_date,'%Y-%m-%d')
            en_date = datetime.datetime.strptime(self_obj.end_date,'%Y-%m-%d')
            st_day = week_number[st_date.strftime('%a')]
            for line in self_obj.time_table_lines:
                if int(line.day) == st_day:
                    self.gen_datewise(cr, uid, line, st_date, en_date, self_obj, context=context)
                if int(line.day) < st_day:
                    new_st_date = st_date - datetime.timedelta(days=(st_day - int(line.day)))
                    self.gen_datewise(cr, uid, line, new_st_date, en_date, self_obj, context=context)
                if int(line.day) > st_day:
                    new_st_date = st_date + datetime.timedelta(days=(int(line.day) - st_day ))
                    self.gen_datewise(cr, uid, line, new_st_date, en_date, self_obj, context=context)

        return {'type': 'ir.actions.act_window_close'}

generate_time_table()
class generate_time_table_line(osv.osv_memory):
    _name = 'gen.time.table.line'
    _description = 'Generate Time Table Lines'
    _rec_name = 'day'

    _columns = {
        'gen_time_table': fields.many2one('generate.time.table', 'Time Table', required=True ),
        'faculty_id': fields.many2one('op.faculty', 'Faculty', required=True ),
        'subject_id': fields.many2one('op.subject', 'Subject', required=True ),
        'day':fields.selection([
                    ('1','Monday'),
                    ('2','Tuesday'),
                    ('3','Wednesday'),
                    ('4','Thursday'),
                    ('5','Friday'),
                    ('6','Saturday'),
                    ('7','Sunday'),
        ],'Day', required=True),
        'period_id': fields.many2one('op.period', 'Period',  required=True),
    }

generate_time_table_line()



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
