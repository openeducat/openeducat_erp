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


class OpSubjectRegistration(models.Model):
    _name = 'op.subject.registration'
    _inherit = ['mail.thread']

    name = fields.Char('Name', readonly=True, default='New')
    student_id = fields.Many2one('op.student', 'Student', required=True,
                                 track_visibility='onchange')
    course_id = fields.Many2one('op.course', 'Course', required=True,
                                track_visibility='onchange')
    batch_id = fields.Many2one('op.batch', 'Batch', required=True,
                               track_visibility='onchange')
    compulsory_subject_ids = fields.Many2many(
        'op.subject', 'subject_compulsory_rel',
        'register_id', 'subject_id', string="Compulsory Subjects",
        readonly=True)
    elective_subject_ids = fields.Many2many(
        'op.subject', string="Elective Subjects")
    state = fields.Selection([
        ('draft', 'Draft'), ('submitted', 'Submitted'),
        ('approved', 'Approved'), ('rejected', 'Rejected')],
        default='draft', string='state', copy=False,
        track_visibility='onchange')
    max_unit_load = fields.Float('Maximum Unit Load',
                                 track_visibility='onchange')
    min_unit_load = fields.Float('Minimum Unit Load',
                                 track_visibility='onchange')

    @api.one
    def action_reset_draft(self):
        self.state = 'draft'
        return True

    @api.one
    def action_reject(self):
        self.state = 'rejected'
        return True

    @api.one
    def action_approve(self):
        subject_ids = []
        for sub in self.compulsory_subject_ids:
            subject_ids.append(sub.id)
        for sub in self.elective_subject_ids:
            subject_ids.append(sub.id)
        course_ids = self.env['op.student.course'].search([
            ('student_id', '=', self.student_id.id),
            ('course_id', '=', self.course_id.id)
        ])
        course_ids[0].write({
            'subject_ids': [[6, 0, list(set(subject_ids))]]
        })
        self.state = 'approved'
        return True

    @api.one
    def action_submitted(self):
        self.state = 'submitted'
        return True

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'op.subject.registration') or '/'
        return super(OpSubjectRegistration, self).create(vals)

    @api.one
    def get_subjects(self):
        subject_ids = []
        if self.course_id and self.course_id.subject_ids:
            for subject in self.course_id.subject_ids:
                if subject.subject_type == 'compulsory':
                    subject_ids.append(subject.id)
        self.compulsory_subject_ids = [(6, 0, subject_ids)]
