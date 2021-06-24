# -*- coding: utf-8 -*-
#/#############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2004-TODAY OpenEduCat Inc(<http://www.OpenEduCat Inc.com>).
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
