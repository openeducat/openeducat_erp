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

import time
from osv import osv
from report import report_sxw
import netsvc

class admission_analysis_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context={}):
        super(admission_analysis_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_date':self.get_date,
            'get_data':self.get_data,
        })
        
    def get_date(self, data):
        start_date = data['start_date']
        end_date = data['end_date']
        print "___________date__________",'From'+ start_date + ' To ' + end_date
        return 'From' + start_date + ' To ' + end_date
        
    def get_data(self, data):
        print "_________data_______________",data['course_id'][0]
        lst = []
        student_pool = self.pool.get('op.admission')
        student_search = student_pool.search(self.cr, self.uid, [('state', '=', 'done'),
                                                        ('course_id', '=', data['course_id'][0]), 
                                                        ('standard_id', '=', data['standard_id'][0]), 
                                                        ('admission_date', '>=', data['start_date']), 
                                                        ('admission_date', '<=', data['end_date'])],
                                                            order= 'admission_date desc')
        print "_____________student__search_______________",student_search
        res = {}
        res1 = {}
        total_student = 0
        for student in student_pool.browse(self.cr, self.uid, student_search):
            print "___________student.name______________",student
            total_student += 1
            res = {
                   'name': student.name,
                   'middle_name': student.middle_name,
                   'last_name': student.last_name,
                   'category': student.category_id.name,
                   'application_no': student.application_number,
                   }
            lst.append(res)
        res1['total'] = total_student
        lst.append(res1)
        print "***************************"
        print lst
        print "***************************"
        return lst

report_sxw.report_sxw('report.admission.analysis', 'op.admission','addons/openeducat_erp/report/admission_analysis_report.rml',
                      parser=admission_analysis_report, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
