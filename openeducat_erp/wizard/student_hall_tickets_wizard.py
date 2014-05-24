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
from openerp.tools.translate import _
import time

class student_hall_ticket(osv.osv_memory):
    """ Retrun Book Wizard """

    _name = 'student.hall.ticket'

    _columns = {
                'exam_session_id':fields.many2one('op.exam.session','Exam Session', required=True),
                
                }
    
    def print_report(self, cr, uid, ids, context={}):
        
        data = self.read(cr, uid, ids, ['exam_session_id'])
        return {
                'type': 'ir.actions.report.xml',
                'report_name': 'student.hall.ticket',
                'datas': data[0],
        }

student_hall_ticket()