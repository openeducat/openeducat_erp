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
from osv import osv, fields
from tools.translate import _
import time

class admission_analysis(osv.osv_memory):
    """ Admission Analysis Wizard """

    _name = 'admission.analysis'

    _columns = {
                'course_id': fields.many2one('op.course', 'Course', required=True),
                'standard_id': fields.many2one('op.standard', 'Standard', required=True),
                'start_date': fields.date('Start Date', required=True),
                'end_date': fields.date('End Date', required=True),
                }
    
    _defaults = {
                 'start_date': time.strftime('%Y-%m-01'),
            }
    
    def print_report(self, cr, uid, ids, context={}):
        
        data = self.read(cr, uid, ids, ['course_id', 'standard_id', 'start_date', 'end_date'])
        return {
                'type': 'ir.actions.report.xml',
                'report_name': 'admission.analysis',
                'datas': data[0],
        }

admission_analysis()