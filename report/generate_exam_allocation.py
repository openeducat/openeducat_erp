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
import datetime
from osv import osv, fields
from report import report_sxw



class exam_allocation_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(exam_allocation_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'gen_exam_seat':self.gen_exam_seat,
        })
    

    def gen_exam_seat(self, data):
        print '________DATA________',data
        lst_main = []
        session_pool = self.pool.get('op.exam.session')
        student_pool = self.pool.get('op.student')
        
        session_search = session_pool.search(self.cr, self.uid, [('room_id','=',data['room_id'][1])])
        for session_obj in session_search:
            dic_main = {}
            session_browse = session_pool.browse(self.cr, self.uid, session_obj)
            student_search = student_pool.search(self.cr, self.uid, [('course_id','=',session_browse.course_id.id)])
            lst_student = []
            for student_obj in student_search:
                dic_student ={}
                student_browse = student_pool.browse(self.cr, self.uid, student_obj)
                dic_student ={
                              'student': student_browse.name,
                              'roll_no': student_browse.roll_number,
                              'course': student_browse.course_id.name,
                              'standard': student_browse.standard_id.name
                              }
                lst_student.append(dic_student)
                lst_exam = []
                for exam in session_browse.exam_ids:
                    dic_exam = {}
                    dic_exam ={
                               'exam' : exam.name,
                               'students': lst_student 
                               }
                    lst_exam.append(dic_exam)
                dic_main = {
                       'exam_session':session_browse.name,
                       'exams': lst_exam
                       }
                lst_main.append(dic_main)
                print '_________lst_main_______',lst_main
                
        return lst_main  
     

report_sxw.report_sxw('report.op.exam.allocation','op.exam.res.allocation', 
                      'addons/openeducat_erp/report/generate_exam_allocation.rml', 
                      parser=exam_allocation_report, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
