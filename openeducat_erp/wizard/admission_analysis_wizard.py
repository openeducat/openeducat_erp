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
    
    
    def print_report(self, cr, uid, ids, data, context=None):
        if context is None:
            context = {}
        data.update(self.read(cr, uid, ids, ['course_id', 'standard_id', 'start_date', 'end_date'])[0])
        return self.pool['report'].get_action(cr, uid, [], 'openeducat_erp.report_admission_analysis', data=data, context=context)
    
    

admission_analysis()