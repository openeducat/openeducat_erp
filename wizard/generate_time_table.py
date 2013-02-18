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

class generate_time_table(osv.osv_memory):
    _name = 'generate.time.table'
    _description = 'Generate Time Table'
    _rec_name = 'standard_id'

    _columns = {
        'standard_id': fields.many2one('op.standard', 'Standard', required=True),
        'division_id': fields.many2one('op.division', 'Division',  required=True),
        'time_table_lines':fields.one2many('gen.time.table.line','gen_time_table','Time Table Lines', required=True),
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
            dt_st = utils.server_to_local_timestamp(curr_date.strftime("%Y-%m-%d ") + per_time, "%Y-%m-%d %H:%M:%S",
                                     "%Y-%m-%d %H:%M:%S",
                                                    'GMT',
                                     server_tz = context.get('tz','GMT'),

                                     )
            curr_date = datetime.datetime.strptime(dt_st, "%Y-%m-%d %H:%M:%S")
            end_time = datetime.timedelta(hours=line.period_id.duration)
            cu_en_date = curr_date + end_time
            a = time_pool.create(cr, uid, {
                        'faculty_id':line.faculty_id.id,
                        'subject_id':line.subject_id.id,
                        'standard_id':self_obj.standard_id.id,
                        'period_id':line.period_id.id,
                        'division_id':self_obj.division_id.id,
                        'start_datetime':curr_date.strftime("%Y-%m-%d %H:%M:%S"),
                        'end_datetime':cu_en_date.strftime("%Y-%m-%d %H:%M:%S"),
                        })
            print "__________a______________",a

            curr_date = curr_date+ datetime.timedelta(days=day_cnt)

        return True
    def act_gen_time_table(self, cr, uid, ids, context={}):
        for self_obj in self.browse(cr, uid, ids, context=context):
            st_date = datetime.datetime.strptime(self_obj.start_date,'%Y-%m-%d')
            en_date = datetime.datetime.strptime(self_obj.end_date,'%Y-%m-%d')
            st_day = week_number[st_date.strftime('%a')]
            for line in self_obj.time_table_lines:
                print "__________line_____________",line
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
