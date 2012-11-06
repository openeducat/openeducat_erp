# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
##############################################################################

import time
from datetime import datetime
from report import report_sxw

class exam_student_lable_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(exam_student_lable_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_student_data':self.get_student_data
        })
        
    def format_list(self,temp_list):
        cnt = 1
        temp = {}
        lst = []
#        temp_list.sort()
        print "__________temp_list___sort_____",temp_list
        for i in temp_list:
            print "_________i__________",i
            if cnt <= 3:
                temp.update({str(cnt): i})
                cnt += 1
            else:
                cnt = 1
                lst.append(temp)
                temp = {}
                temp.update({str(cnt): i})
                cnt += 1
        print "00000000000000000",len(temp_list)%3
        index = len(temp_list) - len(temp_list)%3    
        if len(temp_list)%3 == 1:
            lst.append({'1': temp_list[index]})
        elif len(temp_list)%3 == 2:
            lst.append({'1': temp_list[index],'2': temp_list[index+1]})
        else:
            lst.append({'1': temp_list[-3],'2': temp_list[-2],'3': temp_list[-1]})
            print "22222222222222",lst
        return lst
    
    
    def get_student_data(self, exam_session_ids):
        final_list = []
        student_pool = self.pool.get('op.student')
        for line in exam_session_ids:
            student_ids = student_pool.search(self.cr, self.uid, [('course_id', '=', line.course_id.id),
                                                                  ('standard_id', '=', line.standard_id.id),
                                                                  ('division_id', '=', line.division_id.id)], order= 'id asc')
            print "______________student_ids_________________",student_ids
            temp_list = []
            for student in student_pool.browse(self.cr, self.uid, student_ids):
                res={
                       'student_name': student.name,
                       'roll_number': student.roll_number,
                       'std': student.standard_id.name
                       }
                temp_list.append(res)
            ret_list = self.format_list(temp_list)
#        print "_________sadasd________",ret_list
#        ret_list.sort()
#        print "_________sort________",ret_list
        return ret_list

report_sxw.report_sxw('report.op.exam.student.lable','op.exam.res.allocation', 'addons/openeducat_erp/report/exam_student_lable.rml', parser=exam_student_lable_report, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
