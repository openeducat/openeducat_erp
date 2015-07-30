# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
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
###############################################################################

from openerp import models, fields, api


class OpResultTemplate(models.Model):
    _name = 'op.result.template'
    _description = 'Result Template'
    _rec_name = 'name'

    exam_session_id = fields.Many2one(
        'op.exam.session', 'Exam Session', required=True)
    name = fields.Char("Name", size=254, required=True)
    result_date = fields.Date('Result Date', required=True)
    line_ids = fields.One2many('op.result.template.line', 'result_id', 'Lines')
    criteria_ids = fields.Many2many(
        'op.min.clear.criteria', string='Minimum qualification Criteria')
    pass_status_ids = fields.Many2many('op.pass.status', string='Pass Status')

    @api.one
    def generate_result(self):
        marksheet_reg_id = self.env['op.marksheet.register'].create({
            'name': 'Mark Sheet for %s' % self.exam_session_id.name,
            'exam_session_id': self.exam_session_id.id,
            'generated_date': fields.Date.today(),
            'generated_by': self.env.uid,
            'status': 'd',
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
                        'status': attd.marks >= exam.pass_marks and 'p' or 'f',
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
                if x[1]['status'] == 'f':
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


class OpResultTemplateLine(models.Model):
    _name = 'op.result.template.line'
    _rec_name = 'exam_session_id'
    _description = 'Result template Line'

    exam_session_id = fields.Many2one('op.exam.session', 'Exam Session')
    detailed_report = fields.Boolean('Detailed Report')
    course_id = fields.Many2one(
        'op.course', 'Course', related='exam_session_id.course_id',
        readonly=True)
    batch_id = fields.Many2one(
        'op.batch', 'Batch', related='exam_session_id.batch_id', readonly=True)
    standard_id = fields.Many2one(
        'op.standard', 'Standard', related='exam_session_id.standard_id',
        readonly=True)
    division_id = fields.Many2one(
        'op.division', 'Division', related='exam_session_id.division_id',
        readonly=True)
    result_id = fields.Many2one('op.result.template', 'Result Template Line')
    exam_lines = fields.One2many(
        'op.result.exam.line', 'result_id', 'Exam Lines')

    @api.onchange('exam_session_id')
    def onchange_exam_session(self):
        ret_val = []
        for exam_obj in self.exam_session_id.exam_ids:
            ret_val.append({'exam_id': exam_obj.id, 'weightage': 100})
        self.exam_lines = ret_val


class OpResultExamLine(models.Model):
    _name = 'op.result.exam.line'
    _description = 'Result Exam Line'

    result_id = fields.Many2one('op.result.template.line', 'Session Template')
    exam_id = fields.Many2one('op.exam', 'Exam')
    pass_marks = fields.Float(
        'Passing Marks', related='exam_id.min_marks', readonly=True)
    total_marks = fields.Float(
        'Total Marks', related='exam_id.total_marks', readonly=True)
    weightage = fields.Float('Weightage')
    result_lines = fields.One2many(
        'op.result.line', 'exam_tmpl_id', 'Result Lines')


class OpMinClearanceCriteria(models.Model):
    _name = "op.min.clear.criteria"

    name = fields.Char('Name', size=256)
    number = fields.Float('Number of Failed Subject')
    result = fields.Char('Result to display')


class OpPassStatus(models.Model):
    _name = 'op.pass.status'
    _description = 'Pass Status'

    name = fields.Char('Name', size=256)
    number = fields.Float('Minimum Percentage')
    result = fields.Char('Result to display')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
