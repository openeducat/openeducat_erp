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
from osv import osv
from osv import fields
import time
class op_result_template(osv.osv):
    _name = 'op.result.template'
    _description = 'Result Template'

    _rec_name = 'name'
    _columns = {
        'exam_session_id':fields.many2one('op.exam.session','Exam Session', required=True),
        'name':fields.char("Name", size=254, required=True),
        'result_date':fields.date('Result Date', required=True),
        'line_ids':fields.one2many('op.result.template.line', 'result_id', 'Lines'),
        'criteria_ids':fields.many2many('op.min.clear.criteria','op_res_tmp_crirel','res_id','cri_id','Minimum qualification Criteria'),
        'pass_status_ids':fields.many2many('op.pass.status','op_res_pass_st_rel','res_id','pass_id','Pass Status')

    }
    def genrate_result(self, cr, uid, ids, context={}):
        for self_obj in self.browse(cr, uid, ids, context=context):

            marksheet_reg_id = self.pool.get('op.marksheet.register').create(cr, uid, {
                            'name':'Mark Sheet for %s'%self_obj.exam_session_id.name,
                            'exam_session_id':self_obj.exam_session_id.id,
                            'generated_date':time.strftime("%Y-%m-%d"),
                            'generated_by':uid,
                            'status':'d',
            })
            stu_lst = []
            for exam_session in self_obj.line_ids:

                total_exam = 0.0
                for exam in exam_session.exam_lines:
                    total_exam += exam.exam_id.total_marks

                    for attd in exam.exam_id.attendees_line:
                        print "55555555555555%",(exam.weightage/100)*attd.marks,attd.student_id.name
                        result_dict = {
                            'exam_id':exam.exam_id.id,
                            'exam_tmpl_id':exam.id,
                            'marks':(exam.weightage/100)*attd.marks,
                            'status':attd.marks >= exam.pass_marks and 'p' or 'f',
                            'per':(100*attd.marks)/exam.total_marks,
                            'student_id':attd.student_id.id,
                            'total_marks': (exam.weightage/100)*exam.total_marks,
                        }
                        ret_id = self.pool.get('op.result.line').create(cr, uid, result_dict, context=context)
                        stu_lst.append([ret_id,attd.student_id.id,result_dict])
            stu_dict = {}
            for ret_id,stu_id,data in stu_lst:
                if  stu_id not in stu_dict:
                    stu_dict[stu_id] = []

                stu_dict[stu_id].append([ret_id,data])
            for stu_id in stu_dict:


                total_marks = sum([x[1]['marks'] for x in stu_dict[stu_id]])
                print '5555555555%',total_marks
                per = (total_exam and (100/total_exam)*total_marks) or 0.0
                result = ''
                pass_flg = True
                number_fail = 0
                for x in stu_dict[stu_id]:
                    if x[1]['status'] == 'f':
                        pass_flg = False
                        number_fail += 1
                if pass_flg:

                    pass_st_ids = self_obj.pass_status_ids
                    to_consider = False
                    min_pass = 0.0

                    for pass_st in pass_st_ids:
                        if pass_st.number <= per and pass_st.number > min_pass:
                            min_pass = pass_st.number
                            to_consider = pass_st

                    if to_consider:
                        result  = to_consider.result
                else:
                    crit_ids = self_obj.criteria_ids
                    to_consider = False
                    max_pass = False
                    for crit_id in crit_ids:
                        if crit_id.number == number_fail:
                            to_consider = crit_id
                        if not max_pass or  crit_id.number > max_pass.number:
                            max_pass = crit_id
                    if not to_consider:
                        to_consider = max_pass
                    result = to_consider.result

                mark_line_id = self.pool.get('op.marksheet.line').create(cr, uid,
                                                                         {'student_id':stu_id,
                                                                          'marksheet_reg_id':marksheet_reg_id,
                                                                          'exam_session_id':exam_session.id,
                                                                          'result':result,
                                                                          'total_marks': total_marks,
                                                                          'total_per': per,
                                                                          'total_exam_marks':total_exam,
                                                                         }
                                                                        )
                self.pool.get('op.result.line').write(cr, uid, [x[0] for x in stu_dict[stu_id]], {'result_id':mark_line_id,
                                                                                                 })
        return True


op_result_template()

class op_result_template_line(osv.osv):
    _name = 'op.result.template.line'
    _rec_name = 'exam_session_id'
    _description = 'Result template Line'

    _columns = {
        'exam_session_id':fields.many2one('op.exam.session','Exam Session'),
        'detailed_report':fields.boolean('Detailed Report'),
        'course_id': fields.related('exam_session_id', 'course_id', type='many2one', relation='op.course',
                            string='Course', readonly=True ),
        'batch_id': fields.related('exam_session_id', 'batch_id', type='many2one', relation='op.batch',
                            string='Batch', readonly=True ),
        'standard_id':fields.related('exam_session_id', 'standard_id', type='many2one',
                             relation='op.standard', string="Standard", readonly=True),
        'division_id': fields.related('exam_session_id', 'division_id', type='many2one', relation='op.division',
                            string='Division', readonly=True ),
        'result_id':fields.many2one('op.result.template','Result Template Line'),
        'exam_lines':fields.one2many('op.result.exam.line', 'result_id', 'Exam Lines'),
    }
    def onchange_exam_session(self, cr, uid, ids, exam_session_id, context={}):
        ret_val = []
        exam_session_pool = self.pool.get('op.exam.session')
        exam_session_obj = exam_session_pool.browse(cr, uid, exam_session_id, context=context)
        for exam_obj in exam_session_obj.exam_ids:
            ret_val.append({'exam_id':exam_obj.id,'weightage':100})

        return {'value':{'exam_lines':ret_val}}

op_result_template_line()

class op_result_exam_line(osv.osv):
    _name = 'op.result.exam.line'
    _description = 'Result Exam Line'

    _columns = {
        'result_id':fields.many2one('op.result.template.line'),
        'exam_id':fields.many2one('op.exam', 'Exam'),
        'pass_marks':fields.related('exam_id',
                                    'min_marks',
                                    type='float',
                                    string='Passing Marks',
                                    readonly=True),
        'total_marks':fields.related('exam_id',
                                     'total_marks',
                                     type='float',
                                     string='Total Marks',
                                     readonly=True),
        'weightage':fields.float('Weightage'),
        'result_lines':fields.one2many("op.result.line",
                                       "exam_tmpl_id",
                                       "Result Lines"),
    }

op_result_exam_line()

class op_min_clearance_criteria(osv.osv):

    _name = "op.min.clear.criteria"
    _columns = {
        'name':fields.char('Name', size=256),
        'number':fields.float('Number of Failed Subject'),
        'result':fields.char('Result to display'),
    }

op_min_clearance_criteria()

class op_pass_status(osv.osv):

    _name = 'op.pass.status'
    _description = 'Pass Status'

    _columns = {
        'name':fields.char('Name', size=256),
        'number':fields.float('Minimum Percentage'),
        'result':fields.char('Result to display'),
    }

op_pass_status()


