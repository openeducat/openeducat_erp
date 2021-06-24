# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
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

from openerp import models, fields


class OpPeriod(models.Model):
    _name = 'op.period'
    _description = 'Period'
    _order = 'sequence'

    name = fields.Char('Name', size=16, required=True)
    hour = fields.Selection([
        ('1', '1'), ('2', '2'), ('3', '3'),
        ('4', '4'), ('5', '5'), ('6', '6'),
        ('7', '7'), ('8', '8'), ('9', '9'),
        ('10', '10'), ('11', '11'), ('12', '12')
    ], 'Hours', required=True)
    minute = fields.Selection([
        ('00', '00'), ('15', '15'),
        ('30', '30'), ('45', '45'),
    ], 'Minute', required=True)
    duration = fields.Float('Duration')
    am_pm = fields.Selection(
        [('am', 'AM'), ('pm', 'PM')], 'AM/PM', required=True)
    sequence = fields.Integer('Sequence')


class OpTimetable(models.Model):
    _name = 'op.timetable'
    _description = 'Time Table'
    _rec_name = 'faculty_id'

    period_id = fields.Many2one('op.period', 'Period', required=True)
    start_datetime = fields.Datetime('Start', required=True)
    end_datetime = fields.Datetime('End', required=True)
    course_id = fields.Many2one('op.course', 'Course', required=False)
    faculty_id = fields.Many2one('op.faculty', 'Faculty', required=True)
    standard_id = fields.Many2one('op.standard', 'Standard', required=True)
    division_id = fields.Many2one('op.division', 'Division', required=True)
    subject_id = fields.Many2one('op.subject', 'Subject', required=True)
    color = fields.Integer('Color Index')
    type = fields.Selection(
        [('Monday', 'Monday'), ('Tuesday', 'Tuesday'),
         ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'),
         ('Friday', 'Friday'), ('Saturday', 'Saturday')], 'Days')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
