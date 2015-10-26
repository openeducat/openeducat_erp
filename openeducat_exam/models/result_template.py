# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from openerp import models, fields, api


class OpResultTemplate(models.Model):
    _name = 'op.result.template'
    _description = 'Result Template'
    _rec_name = 'name'

    exam_session_id = fields.Many2one(
        'op.exam.session', 'Exam Session', required=True)
    name = fields.Char("Name", size=254, required=True)
    result_date = fields.Date(
        'Result Date', required=True, default=fields.Date.today())
    line_ids = fields.One2many(
        'op.result.template.line', 'result_id', 'Session Lines')
    criteria_ids = fields.Many2many(
        'op.min.clear.criteria', string='Minimum Qualification Criteria')
    pass_status_ids = fields.Many2many('op.pass.status', string='Pass Status')

    @api.one
    def generate_result(self):
        marksheet_reg_id = self.env['op.marksheet.register'].create({
            'name': 'Mark Sheet for %s' % self.exam_session_id.name,
            'exam_session_id': self.exam_session_id.id,
            'generated_date': fields.Date.today(),
            'generated_by': self.env.uid,
            'status': 'draft',
        })
        student_list = []
        for exam_session in self.line_ids:
            total_exam = 0.0
            for exam in exam_session.exam_lines:
                total_exam += exam.exam_id.total_marks

                for attd in exam.exam_id.attendees_line:
                    result_dict = {
                        'exam_id': exam.exam_id.id,
                        'exam_tmpl_id': exam.id,
                        'marks': (exam.weightage / 100) * attd.marks,
                        'status': attd.marks >= exam.pass_marks and
                        'pass' or 'fail',
                        'per': (100 * attd.marks) / exam.total_marks,
                        'student_id': attd.student_id.id,
                        'total_marks': (exam.weightage / 100) *
                        exam.total_marks,
                    }
                    ret_id = self.env['op.result.line'].create(result_dict)
                    student_list.append(
                        [ret_id, attd.student_id.id, result_dict])
        stu_dict = {}
        for ret_id, stu_id, data in student_list:
            if stu_id not in stu_dict:
                stu_dict[stu_id] = []

            stu_dict[stu_id].append([ret_id, data])
        for stu_id in stu_dict:

            total_marks = sum([x[1]['marks'] for x in stu_dict[stu_id]])
            per = (total_exam and (100 / total_exam) * total_marks) or 0.0
            result = ''
            pass_flg = True
            number_fail = 0
            for x in stu_dict[stu_id]:
                if x[1]['status'] == 'fail':
                    pass_flg = False
                    number_fail += 1
            if pass_flg:

                pass_st_ids = self.pass_status_ids
                to_consider = False
                min_pass = 0.0

                for pass_st in pass_st_ids:
                    if pass_st.number <= per and pass_st.number > min_pass:
                        min_pass = pass_st.number
                        to_consider = pass_st

                if to_consider:
                    result = to_consider.result
            else:
                crit_ids = self.criteria_ids
                to_consider = False
                max_pass = False
                for crit_id in crit_ids:
                    if crit_id.number == number_fail:
                        to_consider = crit_id
                    if not max_pass or crit_id.number > max_pass.number:
                        max_pass = crit_id
                if not to_consider:
                    to_consider = max_pass
                result = to_consider.result
            mark_line_id = self.env['op.marksheet.line'].create(
                {'student_id': stu_id,
                 'marksheet_reg_id': marksheet_reg_id.id,
                 'exam_session_id': exam_session.id,
                 'result': result,
                 'total_marks': total_marks,
                 'total_per': per,
                 'total_exam_marks': total_exam,
                 })
            self.env['op.result.line'].browse(
                [x[0].id for x in stu_dict[stu_id]]).write(
                {'result_id': mark_line_id.id})
        return True


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
