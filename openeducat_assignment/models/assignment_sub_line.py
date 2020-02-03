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


class OpAssignmentSubLine(models.Model):
    _name = "op.assignment.sub.line"
    _inherit = "mail.thread"
    _rec_name = "assignment_id"
    _description = "Assignment Submission"
    _order = "submission_date DESC"

    def _compute_get_user_group(self):
        for user in self:
            if self.env.user.has_group(
                    'openeducat_core.group_op_back_office_admin') or \
                    self.env.user.has_group(
                        'openeducat_core.group_op_back_office') or \
                    self.env.user.has_group(
                        'openeducat_core.group_op_faculty'):
                user.user_boolean = True
            else:
                user.user_boolean = False

    assignment_id = fields.Many2one(
        'op.assignment', 'Assignment', required=True)
    student_id = fields.Many2one(
        'op.student', 'Student',
        default=lambda self: self.env['op.student'].search(
            [('user_id', '=', self.env.user.id)]), required=True)
    description = fields.Text('Description', track_visibility='onchange')
    state = fields.Selection([
        ('draft', 'Draft'), ('submit', 'Submitted'), ('reject', 'Rejected'),
        ('change', 'Change Req.'), ('accept', 'Accepted')], basestring='State',
        default='draft', track_visibility='onchange')
    submission_date = fields.Datetime(
        'Submission Date', readonly=True,
        default=lambda self: fields.Datetime.now(), required=True)
    marks = fields.Float('Marks', track_visibility='onchange')
    note = fields.Text('Note')
    user_id = fields.Many2one(
        'res.users', related='student_id.user_id', string='User')
    faculty_user_id = fields.Many2one(
        'res.users', related='assignment_id.faculty_id.user_id',
        string='Faculty User')
    user_boolean = fields.Boolean(string='Check user',
                                  compute='_compute_get_user_group')
    active = fields.Boolean(default=True)

    def act_draft(self):
        result = self.state = 'draft'
        return result and result or False

    def act_submit(self):
        result = self.state = 'submit'
        return result and result or False

    def act_accept(self):
        result = self.state = 'accept'
        return result and result or False

    def act_change_req(self):
        result = self.state = 'change'
        return result and result or False

    def act_reject(self):
        result = self.state = 'reject'
        return result and result or False

    def unlink(self):
        for record in self:
            if not record.state == 'draft' and not self.env.user.has_group(
                    'openeducat_core.group_op_faculty'):
                raise ValidationError(
                    _("You can't delete none draft submissions!"))
        res = super(OpAssignmentSubLine, self).unlink()
        return res

    @api.model
    def create(self, vals):
        if self.env.user.child_ids:
            raise Warning(_('Invalid Action!\n Parent can not \
            create Assignment Submissions!'))
        return super(OpAssignmentSubLine, self).create(vals)

    def write(self, vals):
        if self.env.user.child_ids:
            raise Warning(_('Invalid Action!\n Parent can not edit \
            Assignment Submissions!'))
        return super(OpAssignmentSubLine, self).write(vals)
