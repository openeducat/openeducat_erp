###############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<https://www.openeducat.org>).
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

import time

from odoo import api, fields, models


class StudentAttendanceReport(models.AbstractModel):
    _name = "report.openeducat_attendance.student_attendance_report"
    _description = "Attendance Report"

    def _get_absences(self, student_id, from_date, to_date):
        """Return list of attendance records for student between dates.

        Use the stored attendance_date on op.attendance.line so we can filter
        at the DB level. Remark is set to one of: Present, Excused, Absent, Late.
        """
        if not student_id:
            return []

        # build domain using the stored attendance_date field (avoids dotted domains)
        domain = [('student_id', '=', student_id)]
        if from_date:
            domain.append(('attendance_date', '>=', from_date))
        if to_date:
            domain.append(('attendance_date', '<=', to_date))

        lines = self.env['op.attendance.line'].search(
            domain, order='attendance_date asc')

        absences = []
        for line in lines:
            absent_date = line.attendance_date or False
            # priority: present -> excused -> absent -> late
            if line.present:
                remark = 'Present'
            elif line.excused:
                remark = 'Excused'
            elif line.absent:
                remark = 'Absent'
            elif line.late:
                remark = 'Late'

            absences.append({
                'absent_date': absent_date,
                'present': bool(line.present),
                'remark': remark,
            })

        # sort (already ordered by attendance_date from search, keep fallback)
        absences.sort(key=lambda x: (x['absent_date'] is False, x['absent_date'] or fields.Date.to_string(fields.Date.context_today(self)))) # noqa
        return absences

    @api.model
    def _get_report_values(self, docids, data=None):
        data = data or {}
        student_id = data.get('student_id')
        from_date = data.get('from_date')
        to_date = data.get('to_date')

        student = self.env['op.student'].browse(student_id) if student_id else None
        absences = self._get_absences(student_id, from_date, to_date)

        # docs: keep original behaviour if a model is provided in context
        model = self.env.context.get('active_model')
        docs = (self.env[model].browse(docids)
                if model and docids
                else self.env[model].browse(self.env.context.get('active_id'))
                if model
                else self.env['res.partner'].browse([]))

        # counts by remark
        present_count = sum(1 for a in absences if a.get('remark') == 'Present')
        excused_count = sum(1 for a in absences if a.get('remark') == 'Excused')
        absent_count = sum(1 for a in absences if a.get('remark') == 'Absent')
        late_count = sum(1 for a in absences if a.get('remark') == 'Late')

        return {
            'doc_ids': docids,
            'doc_model': model or '',
            'docs': docs,
            'time': time,
            'student': student,
            'student_name': student.name if student else '',
            'from_date': from_date,
            'to_date': to_date,
            'absences': absences,
            'present_count': present_count,
            'excused_count': excused_count,
            'absent_count': absent_count,
            'late_count': late_count,
            'total_absences': absent_count,
        }
