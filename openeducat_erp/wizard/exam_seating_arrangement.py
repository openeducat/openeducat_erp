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

from openerp.osv import osv, fields
import time
from datetime import datetime

class exam_seat_arrange(osv.osv_memory):

    _name = 'exam.seat.arrange'
    _columns = {
                'room_id': fields.many2one('op.exam.room', 'Room', required=True),
                'exam_session_ids': fields.many2many('op.exam.session','exam_session_rel1', 'op_exam', 'op_session', 'Select Section', required=True),
                'start_time': fields.datetime('Start Time', required=True),
                'end_time': fields.datetime('End Time', required=True),
                }
    
    _defaults = {
                 'start_time' : fields.date.context_today,
                 'end_time' : fields.date.context_today,
                 }
    
    
    def print_report(self, cr, uid, ids, context=None):
        
        data = self.read(cr, uid, ids, ['room_id','start_time','end_time','exam_session_ids'], context=context)
        return {
                'type': 'ir.actions.report.xml',
                'report_name': 'op.exam.allocation',
                'datas': data[0],
        }
        
    
exam_seat_arrange()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
