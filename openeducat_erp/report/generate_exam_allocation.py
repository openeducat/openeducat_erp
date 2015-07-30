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

import time

from openerp.osv import osv
from openerp.report import report_sxw


class ExamAllocationReport(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        super(ExamAllocationReport, self).__init__(
            cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'gen_exam_seat': self.gen_exam_seat,
        })

    def arrange_list(self, lst_inner, length):
        l = []
        res = []
        if length == 3:
            res = map(
                l.append(lst_inner[0]), lst_inner[0][lst_inner[0].keys()[0]],
                lst_inner[1][lst_inner[1].keys()[0]],
                lst_inner[2][lst_inner[2].keys()[0]])
        elif length == 2:
            res = map(
                l.append(lst_inner[0]), lst_inner[0][lst_inner[0].keys()[0]],
                [], lst_inner[1][lst_inner[1].keys()[0]])
        elif length == 1:
            res = map(
                l.append(lst_inner[0]),
                lst_inner[0][lst_inner[0].keys()[0]], [], [])
        return res

    def gen_exam_seat(self, data):
        final_list = []
        session_pool = self.pool.get('op.exam.session')
        student_pool = self.pool.get('op.student')
        room_pool = self.pool.get('op.exam.room')

        lst_inner = []
        capacity = room_pool.read(
            self.cr, self.uid, data['room_id'][0], ['capacity'])['capacity']
        session_search = session_pool.search(
            self.cr, self.uid, [('room_id', '=', data['room_id'][1]),
                                ('id', 'in', data['exam_session_ids'])])
        for session_obj in session_search:
            dic_inner = {}
            session_browse = session_pool.browse(
                self.cr, self.uid, session_obj)
            student_search = student_pool.search(
                self.cr, self.uid,
                [('course_id', '=', session_browse.course_id.id)])
            if len(student_search) > capacity:
                raise osv.except_osv(
                    ('Error!'), ("Number of students must be less than room \
                     capacity!\n Students %s can not be accomodate in \
                     room %s\n Select another room") % (len(student_search),
                                                        capacity))
            lst_student = []

            for student_obj in student_search:
                dic_student = {}
                student_browse = student_pool.browse(
                    self.cr, self.uid, student_obj)
                dic_student = {
                    'student': student_browse.name,
                    'roll_no': student_browse.roll_number,
                    'course': student_browse.course_id.name,
                    'standard': student_browse.standard_id.name
                }
                lst_student.append(dic_student)
                # TODO: arrange students as per roll number ascending
            dic_inner[str(session_browse.course_id.name)] = lst_student
            lst_inner.append(dic_inner)

        final_list = self.arrange_list(lst_inner, len(session_search))
        return final_list


report_sxw.report_sxw(
    'report.op.exam.allocation', 'op.exam.res.allocation',
    'addons/openeducat_erp/report/generate_exam_allocation.rml',
    parser=ExamAllocationReport, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
