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
class op_period(osv.osv):
    _name = 'op.period'
    _description = 'Period'

    _columns = {
        'name':fields.char('Name',size=16, required=True),
        'hour':fields.selection([
                    ('1','1'), ('2','2'), ('3','3'),
                    ('4','4'), ('5','5'), ('6','6'),
                    ('7','7'), ('8','8'), ('9','9'),
                    ('10','10'), ('11','11'), ('12','12'),
        ],'Hours', required=True),
        'minute':fields.selection([
                    ('00','00'), ('15','15'),
                    ('30','30'), ('45','45'),
        ],'Minute', required=True),
        'duration':fields.float('Duration'),
        'am_pm':fields.selection([('am','AM'),('pm','PM')],'AM/PM', required=True),
    }

op_period()

class op_timetable(osv.osv):
    _name = 'op.timetable'
    _description = 'Time Table'
    _rec_name = 'faculty_id'

    _columns = {
        'period_id': fields.many2one('op.period', 'Period', ),
        'start_datetime':fields.datetime('Start'),
        'end_datetime':fields.datetime('End'),
        'faculty_id': fields.many2one('op.faculty', 'Faculty', ),
        'standard_id': fields.many2one('op.standard', 'Standard', ),
        'division_id': fields.many2one('op.division', 'Division', ),
        'subject_id': fields.many2one('op.subject', 'Subject', ),
    }

op_timetable()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
