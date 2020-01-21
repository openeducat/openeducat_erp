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


class OpAssignment(models.Model):
    _name = "op.assignment"
    _inherit = "mail.thread"
    _description = "Assignment"
    _order = "submission_date DESC"

    name = fields.Char('Name', size=64, required=True)
    course_id = fields.Many2one('op.course', 'Course', required=True)
    batch_id = fields.Many2one('op.batch', 'Batch', required=True)
    subject_id = fields.Many2one('op.subject', 'Subject', required=True)
    faculty_id = fields.Many2one(
        'op.faculty', 'Faculty', default=lambda self: self.env[
            'op.faculty'].search([('user_id', '=', self.env.uid)]),
        required=True)
    assignment_type_id = fields.Many2one(
        'op.assignment.type', 'Assignment Type', required=True)
    marks = fields.Float('Marks', required=True, track_visibility='onchange')
    description = fields.Text('Description', required=True)
    state = fields.Selection([
        ('draft', 'Draft'), ('publish', 'Published'),
        ('finish', 'Finished'), ('cancel', 'Cancel'),
    ], 'State', required=True, default='draft', track_visibility='onchange')
    issued_date = fields.Datetime(string='Issued Date', required=True,
                                  default=lambda self: fields.Datetime.now())
    submission_date = fields.Datetime('Submission Date', required=True,
                                      track_visibility='onchange')
    allocation_ids = fields.Many2many('op.student', string='Allocated To')
    assignment_sub_line = fields.One2many('op.assignment.sub.line',
                                          'assignment_id', 'Submissions')
    reviewer = fields.Many2one('op.faculty', 'Reviewer')
    attachment_ids = fields.One2many('ir.attachment', 'res_id',
                                     domain=[('res_model', '=',
                                              'op.assignment')],
                                     string='Attachments',
                                     readonly=True)

    @api.multi
    @api.constrains('issued_date', 'submission_date')
    def check_dates(self):
        for record in self:
            issued_date = fields.Date.from_string(record.issued_date)
            submission_date = fields.Date.from_string(record.submission_date)
            if issued_date > submission_date:
                raise ValidationError(_(
                    "Submission Date cannot be set before Issue Date."))

    @api.onchange('course_id')
    def onchange_course(self):
        self.batch_id = False
        if self.course_id:
            subject_ids = self.env['op.course'].search([
                ('id', '=', self.course_id.id)]).subject_ids
            return {'domain': {'subject_id': [('id', 'in', subject_ids.ids)]}}

    @api.multi
    def act_publish(self):
        result = self.state = 'publish'
        return result and result or False

    @api.multi
    def act_finish(self):
        result = self.state = 'finish'
        return result and result or False

    @api.multi
    def act_cancel(self):
        self.state = 'cancel'

    @api.multi
    def act_set_to_draft(self):
        self.state = 'draft'

    @api.multi
    def unlink(self):
        for record in self:
            if not record.state == 'draft' and not self.env.user.has_group(
                    'openeducat_core.group_op_faculty'):
                raise ValidationError(
                    _("You can't delete none draft submissions!"))
        res = super(OpAssignment, self).unlink()
        return res

    @api.multi
    def write(self, vals):
        if self.env.user.child_ids:
            raise Warning(_('Invalid Action!\n Parent can not edit \
               Assignment Submissions!'))
        return super(OpAssignment, self).write(vals)

    @api.model
    def create(self, vals):
        res = super(OpAssignment, self).create(vals)
        return res

    def search_read_for_app(self, domain=None, fields=None, offset=0, limit=None, order=None, args=None):
        if self.env.user.partner_id.is_student:
            partner = self.env.user.partner_id
            domain = ([('state', '=', 'publish'), ('allocation_ids.partner_id', '=', partner.id)])
            res = self.sudo().search_read(domain=domain, fields=['name', 'batch_id', 'course_id',
                                                                 'subject_id', 'assignment_type_id',
                                                                 'faculty_id', 'issued_date', 'submission_date',
                                                                 'marks', 'allocation_ids', 'state', 'description', ],
                                          offset=offset, limit=limit, order=order)
            return res

        elif self.env.user.partner_id.is_parent:
            user = self.env.user
            parent_id = self.env['op.parent'].sudo().search([('user_id', '=', user.id)])

            student_id = [student.id for student in parent_id.student_ids]
            domain = [('allocation_ids', 'in', student_id)]
            res = self.sudo().search_read(domain=domain, fields=['name', 'batch_id', 'course_id',
                                                                 'subject_id', 'assignment_type_id',
                                                                 'faculty_id', 'issued_date', 'submission_date',
                                                                 'marks', 'allocation_ids', 'description', ],
                                          offset=offset, limit=limit, order=order)
            return res

        elif self.user_has_groups('openeducat_core.group_op_faculty'):
            user = self.env.user
            faculty_id = self.env['op.faculty'].sudo().search([('user_id', '=', user.id)])
            domain = [('faculty_id', '=', faculty_id.id)]
            res = self.sudo().search_read(domain=domain, fields=['name', 'batch_id', 'course_id',
                                                                 'subject_id', 'assignment_type_id',
                                                                 'faculty_id', 'issued_date', 'submission_date',
                                                                 'marks', 'allocation_ids', 'description', 'state'],
                                          offset=offset, limit=limit, order=order)
            return res
