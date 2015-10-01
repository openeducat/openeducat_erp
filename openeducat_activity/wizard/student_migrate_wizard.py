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
from openerp.exceptions import ValidationError


class StudentMigrate(models.TransientModel):

    """ Student Migration Wizard """
    _name = 'student.migrate'

    date = fields.Date('Date', required=True, default=fields.Date.today())
    course_from_id = fields.Many2one('op.course', 'From Course', required=True)
    course_to_id = fields.Many2one('op.course', 'To Course', required=True)
    student_ids = fields.Many2many(
        'op.student', string='Student(s)', required=True)

    @api.one
    @api.constrains('course_from_id', 'course_to_id')
    def _check_admission_register(self):
        if self.course_from_id == self.course_to_id:
            raise ValidationError("From Course must not be same as To Course!")

        if self.course_from_id.parent_id:
            if self.course_from_id.parent_id != \
                    self.course_to_id.parent_id:
                raise ValidationError(
                    "Can't migrate, As selected courses don't \
                    share same parent course!")
        else:
            raise ValidationError(
                "Can't migrate, Proceed for new admission")

    @api.one
    @api.onchange('course_from_id')
    def onchange_course_id(self):
        self.student_ids = False

    @api.one
    def student_migrate_forward(self):
        activity_type = self.env["op.activity.type"]
        act_type = activity_type.search([('name', '=', 'Migration')], limit=1)
        if not act_type:
            act_type = activity_type.create({'name': 'Migration'})

        for student in self.student_ids:
            activity_vals = {
                'student_id': student.id,
                'type_id': act_type.id,
                'date': self.date
            }
            self.env['op.activity'].create(activity_vals)
            student.write({'course_id': self.course_to_id.id})


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
