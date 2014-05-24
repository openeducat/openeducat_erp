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

class op_period(osv.osv):
    _name = 'op.period'
    _description = 'Period'
    _order = "sequence"

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
        'sequence': fields.integer('Sequence'),
    }

op_period()

class op_timetable(osv.osv):
    _name = 'op.timetable'
    _description = 'Time Table'
    _rec_name = 'faculty_id'

    _columns = {
        'period_id': fields.many2one('op.period', 'Period', required=True),
        'start_datetime':fields.datetime('Start', required=True),
        'end_datetime':fields.datetime('End', required=True),
        'faculty_id': fields.many2one('op.faculty', 'Faculty', required=True),
        'standard_id': fields.many2one('op.standard', 'Standard', required=True),
        'division_id': fields.many2one('op.division', 'Division', required=True),
        'subject_id': fields.many2one('op.subject', 'Subject', required=True),
        'color': fields.integer('Color Index'),
        'type': fields.selection([('Monday', 'Monday'),('Tuesday', 'Tuesday'),('Wednesday', 'Wednesday'),('Thursday', 'Thursday'),('Friday', 'Friday'),('Saturday', 'Saturday')], 'Days'),
    }

op_timetable()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
