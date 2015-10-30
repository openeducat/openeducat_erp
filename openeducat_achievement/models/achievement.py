# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from openerp import models, fields


class OpAchievement(models.Model):
    _name = 'op.achievement'
    _rec_name = 'student_id'

    student_id = fields.Many2one('op.student', 'Student', required=True)
    faculty_id = fields.Many2one('op.faculty', 'Faculty', required=True)
    achievement_type = fields.Many2one(
        'op.achievement.type', 'Achievement Type', required=True)
    description = fields.Text('Description', required=True)
    achievement_date = fields.Date(
        'Date', required=True, default=fields.Date.today())

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
