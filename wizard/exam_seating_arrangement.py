# -*- coding: utf-8 -*-

from osv import osv, fields
import time
from datetime import datetime

class exam_seat_arrange(osv.osv):

    _name = 'exam.seat.arrange'
    _columns = {
                'room_id': fields.many2one('op.exam.room', 'Room'),
                'start_time': fields.datetime('Start Time', required=True),
                'end_time': fields.datetime('End Time', required=True)
                }
    
    _defaults = {
                 'start_time' : fields.date.context_today,
                 'end_time' : fields.date.context_today
                 }
    
    
    def print_report(self, cr, uid, ids, context=None):
        
        data = self.read(cr, uid, ids, ['room_id','start_time','end_time'], context=context)
        return {
                'type': 'ir.actions.report.xml',
                'report_name': 'op.exam.allocation',
                'datas': data[0],
        }
        
    
exam_seat_arrange()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
