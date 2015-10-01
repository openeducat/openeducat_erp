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

from openerp import models, fields, api


class StudentHallTicket(models.TransientModel):

    """ Student Hall Ticket Wizard """
    _name = 'student.hall.ticket'

    exam_session_id = fields.Many2one(
        'op.exam.session', 'Exam Session', required=True)

    @api.multi
    def print_report(self):
        data = self.read(['exam_session_id'])[0]
        return self.env['report'].get_action(
            self, 'openeducat_exam.report_ticket', data=data)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
