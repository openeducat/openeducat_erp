# -*- coding: utf-8 -*-
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

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class StudentMigrate(models.TransientModel):
    """ Student Migration Wizard """
    _name = "student.migrate"
    _description = "Student Migrate"

    date = fields.Date('Date', required=True, default=fields.Date.today())
    course_from_id = fields.Many2one('op.course', 'From Course', required=True)
    course_to_id = fields.Many2one('op.course', 'To Course')
    batch_id = fields.Many2one('op.batch', 'To Batch')
    optional_sub = fields.Boolean("Optional Subjects")
    student_ids = fields.Many2many(
        'op.student', string='Student(s)', required=True)
    course_completed = fields.Boolean(string="Course Completed?")

    @api.onchange('course_from_id')
    def student_by_course(self):
        self.student_ids = False
        if self.course_from_id:
            lists = []
            student_ids = self.env['op.student.course'].search([
                ('course_id', '=', self.course_from_id.id), ('state', '=', 'running')])
            for i in student_ids:
                lists.append(str(i.student_id.id))
            domain = {'student_ids': [('id', 'in', lists)]}
            result = {'domain': domain}
            return result

    @api.constrains('course_from_id', 'course_to_id')
    def _check_admission_register(self):
        for record in self:
            if record.course_from_id == record.course_to_id:
                raise ValidationError(
                    _("From Course must not be same as To Course!"))

            if (record.course_from_id.parent_id and record.course_to_id)\
                    or (record.course_from_id.parent_id and record.course_completed):
                if record.course_to_id:
                    if record.course_from_id.parent_id != \
                            record.course_to_id.parent_id:
                        raise ValidationError(_(
                            "Can't migrate, As selected courses don't \
                            share same parent course!"))
            else:
                raise ValidationError(
                    _("Can't migrate, Proceed for new admission"))

    def student_migrate_forward(self):
        act_type = self.env.ref('openeducat_activity.op_activity_type_3')
        for record in self:
            for student in record.student_ids:
                if self.course_completed:
                    for course_update in student.course_detail_ids:
                        if course_update.course_id == record.course_from_id:
                            course_update.state = 'finished'
                            activity_vals = {
                                'student_id': student.id,
                                'type_id': act_type.id,
                                'date': self.date,
                                'description': _('Migration From {}'
                                                 ' to Completed Course'.
                                                 format(record.course_from_id.name)),
                            }
                            self.env['op.activity'].create(activity_vals)
                else:
                    for course_update in student.course_detail_ids:
                        if course_update.course_id == self.course_from_id:
                            course_update.state = 'finished'

                            activity_vals = {
                                'student_id': student.id,
                                'type_id': act_type.id,
                                'date': self.date,
                                'description': _('Migration from {} to {}'
                                                 .format(record.course_from_id.name,
                                                         record.course_to_id.name))
                            }
                            self.env['op.activity'].create(activity_vals)

                            student_course = self.env['op.student.course'].search(
                                [('student_id', '=', student.id),
                                 ('course_id', '=', record.course_from_id.id)])
                            student_course.create({
                                'student_id': student.id,
                                'course_id': record.course_to_id.id,
                                'batch_id': record.batch_id.id,
                                'subject_ids': record.course_to_id.subject_ids.ids
                            })

                            reg_id = self.env['op.subject.registration'].create({
                                'student_id': student.id,
                                'batch_id': record.batch_id.id,
                                'course_id':
                                    record.course_to_id.id,
                                'min_unit_load':
                                    record.course_to_id.min_unit_load or 0.0,
                                'max_unit_load':
                                    record.course_to_id.max_unit_load or 0.0,
                                'state': 'draft',
                            })
                            reg_id.get_subjects()
                            if not record.optional_sub:
                                reg_id.action_submitted()
                                reg_id.action_approve()
