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


class OpTransportation(models.Model):
    _name = 'op.transportation'

    name = fields.Char('Name', size=64, required=True)
    stop_ids = fields.Many2many('op.stop', string='Stops')
    cost = fields.Float('Cost')
    vehicle_id = fields.Many2one('op.vehicle', 'Vehicle', required=True)
    start_time = fields.Float('Start Time', required=True)
    end_time = fields.Float('End Time', required=True)
    from_stop_id = fields.Many2one('op.stop', 'From', required=True)
    to_stop_id = fields.Many2one('op.stop', 'To', required=True)
    student_ids = fields.Many2many('op.student', string='Student(s)')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
