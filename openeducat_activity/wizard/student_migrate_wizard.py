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

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class StudentMigrate(models.TransientModel):

    """ Student Migration Wizard """
    _name = 'student.migrate'

    date = fields.Date('Date', required=True, default=fields.Date.today())
    course_from_id = fields.Many2one('op.course', 'From Course', required=True)
    course_to_id = fields.Many2one('op.course', 'To Course', required=True)
    batch_id = fields.Many2one('op.batch', 'To Batch')
    optional_sub = fields.Boolean("Optional Subjects")
    student_ids = fields.Many2many(
        'op.student', string='Student(s)', required=True)

    @api.multi
    @api.constrains('course_from_id', 'course_to_id')
    def _check_admission_register(self):
        for record in self:
            if record.course_from_id == record.course_to_id:
                raise ValidationError(_("From Course must not be same \
                as To Course!"))

            if record.course_from_id.parent_id:
                if record.course_from_id.parent_id != \
                        record.course_to_id.parent_id:
                    raise ValidationError(_(
                        "Can't migrate, As selected courses don't \
                        share same parent course!"))
            else:
                raise ValidationError(_(
                    "Can't migrate, Proceed for new admission"))

    @api.onchange('course_from_id')
    def onchange_course_id(self):
        self.student_ids = False

    @api.multi
    def student_migrate_forward(self):
        for record in self:
            activity_type = self.env["op.activity.type"]
            act_type = activity_type.search(
                [('name', '=', 'Migration')], limit=1)
            if not act_type:
                act_type = activity_type.create({'name': 'Migration'})

            for student in record.student_ids:
                activity_vals = {
                    'student_id': student.id,
                    'type_id': act_type.id,
                    'date': self.date,
                    'description': 'Migration From' +
                    record.course_from_id.name +
                    ' to ' + record.course_to_id.name
                }
                self.env['op.activity'].create(activity_vals)
                student_course = self.env['op.student.course'].search(
                    [('student_id', '=', student.id),
                     ('course_id', '=', record.course_from_id.id)])
                student_course.write({'course_id': record.course_to_id.id})
                reg_id = self.env['op.subject.registration'].create({
                    'student_id': student.id,
                    'batch_id': record.batch_id.id,
                    'course_id': record.course_to_id.id,
                    'min_unit_load': record.course_to_id.min_unit_load or 0.0,
                    'max_unit_load': record.course_to_id.max_unit_load or 0.0,
                    'state': 'draft',
                })
                reg_id.get_subjects()
                if not record.optional_sub:
                    reg_id.action_submitted()
                    reg_id.action_approve()
