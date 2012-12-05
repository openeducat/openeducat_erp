# -*- coding: utf-8 -*-

from osv import osv, fields
import time
from datetime import datetime

class student_attendance(osv.osv_memory):

    _name = 'student.attendance'
    _columns = {
                'from_date': fields.date('From Date', required=True),
                'to_date': fields.date('To Date', required=True),
                }
    
    _defaults = {
                 'from_date' : fields.date.context_today,
                 'to_date' : fields.date.context_today,
                 }
    
    
    def print_report(self, cr, uid, ids, context=None):
        
        data = self.read(cr, uid, ids, ['from_date','to_date'], context=context)
        data[0].update({'student_id':context.get('active_ids',[])[0]})

        return {
                'type': 'ir.actions.report.xml',
                'report_name': 'student.attendance',
                'datas': data[0],
        }
        
    
student_attendance()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
