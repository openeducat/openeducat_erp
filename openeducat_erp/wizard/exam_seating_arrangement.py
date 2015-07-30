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

from openerp import models, fields, api


class ExamSeatArrange(models.TransientModel):
    _name = 'exam.seat.arrange'

    room_id = fields.Many2one('op.exam.room', 'Room', required=True)
    exam_session_ids = fields.Many2many(
        'op.exam.session', string='Select Section', required=True)
    start_time = fields.Datetime(
        'Start Time', default=lambda self: fields.Datetime.now(),
        required=True)
    end_time = fields.Datetime(
        'End Time', default=lambda self: fields.Datetime.now(),
        required=True)

    @api.multi
    def print_report(self):
        data = self.read(
            ['room_id', 'start_time', 'end_time', 'exam_session_ids'])
        return {'type': 'ir.actions.report.xml',
                'report_name': 'op.exam.allocation',
                'datas': data[0]}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
