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

from openerp import models, fields, api, _


class StudentMigrate(models.TransientModel):

    """ Student Migration Wizard """
    _name = 'student.migrate'

    date = fields.Date('Date', required=True, default=fields.Date.today())
    course_id = fields.Many2one('op.course', 'Course', required=True)
    from_standard_id = fields.Many2one(
        'op.standard', 'From Standard', required=True)
    to_standard_id = fields.Many2one(
        'op.standard', 'To Standard', required=True)
    student_ids = fields.Many2many(
        'op.student', string='Student(s)', required=True)

    _sql_constraints = [
        ('from_to_standard_check', 'check(from_standard_id != to_standard_id)',
         _("From Student must not be same as To Student !")),
    ]

    @api.one
    def go_forward(self):
        activity_type = self.env["op.activity.type"]
        lst_student = self.to_standard_id.student_ids.ids
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
            student.write({'standard_id': self.to_standard_id.id})
            lst_student.append(student.id)
        self.from_standard_id.student_ids = \
            self.from_standard_id.student_ids - self.student_ids
        self.to_standard_id.write(
            {'student_ids': [(6, 0, lst_student)]})

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
