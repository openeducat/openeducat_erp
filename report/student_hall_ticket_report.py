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
from datetime import date,datetime
import netsvc

class student_hall_ticket_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context={}):
        super(student_hall_ticket_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_data':self.get_data,
        })
        
    def get_subject(self, datas):
        exam = self.pool.get('op.exam')
        lst = []
        for exam_line in datas['exam_ids']:
            print "__________exam_line____________",exam_line.name
            temp_exam = exam.browse(self.cr, self.uid, exam_line)
            res1 = {
                    'subject': exam_line.subject_id.name,
                    'start_date': exam_line.start_time,
                    'end_date': exam_line.end_time,
                    'sup': ''
                    }
            lst.append(res1)
            print "___________res1_____________",lst
        return lst
    
    def get_data(self, data):
        final_lst = []
        exam_session_pool = self.pool.get('op.exam.session')
        exam_student = self.pool.get('op.student')
#        exam = self.pool.get('op.exam')
        print "__________data____________",data['exam_session_id'][0]
        datas = exam_session_pool.browse(self.cr, self.uid, data['exam_session_id'][0])
        student_search = exam_student.search(self.cr, self.uid, [('course_id', '=', datas.course_id.id), ('standard_id', '=', datas.standard_id.id)])
        print "_________student________________",student_search
        print "__________data__fds___________",datas.exam_ids
        for student in exam_student.browse(self.cr, self.uid, student_search) :
            print "_______student__dcsf_____",student.name
            res = {
                   'exam': datas.name,
                   'exam_code': datas.exam_code,
                   'course': datas.course_id.name,
                   'standard': datas.standard_id.name,
                   'student': student.name,
                   'student_middle': student.middle_name,
                   'student_last': student.last_name,
                   'roll_number': student.roll_number,
                   'line': self.get_subject(datas),
                   }
            print "___________res__________",res
            final_lst.append(res)
        print "___________final_lst__________",final_lst
        return final_lst


report_sxw.report_sxw('report.student.hall.ticket', 'op.exam.session','addons/openeducat_erp/report/student_hall_ticket_report.rml',
                      parser=student_hall_ticket_report, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
