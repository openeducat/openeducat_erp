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

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class OpExamSession(models.Model):
    _name = "op.exam.session"
    _inherit = ["mail.thread"]
    _description = "Exam Session"

    name = fields.Char(
        'Exam Session', size=256, required=True, tracking=True)
    course_id = fields.Many2one(
        'op.course', 'Course', required=True, tracking=True)
    batch_id = fields.Many2one(
        'op.batch', 'Batch', required=True, tracking=True)
    exam_code = fields.Char(
        'Exam Session Code', size=16,
        required=True, tracking=True)
    start_date = fields.Date(
        'Start Date', required=True, tracking=True)
    end_date = fields.Date(
        'End Date', required=True, tracking=True)
    exam_ids = fields.One2many(
        'op.exam', 'session_id', 'Exam(s)')
    exam_type = fields.Many2one(
        'op.exam.type', 'Exam Type',
        required=True, tracking=True)
    evaluation_type = fields.Selection(
        [('normal', 'Normal'), ('grade', 'Grade')],
        'Evolution Type', default="normal",
        required=True, tracking=True)
    venue = fields.Many2one(
        'res.partner', 'Venue', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('schedule', 'Scheduled'),
        ('held', 'Held'),
        ('cancel', 'Cancelled'),
        ('done', 'Done')
    ], 'Status', default='draft', tracking=True)
    active = fields.Boolean(default=True)
    exams_count = fields.Integer(
        compute='_compute_exams_count', string="Exams")

    _unique_exam_session_code = models.Constraint(
        'unique(exam_code)', 'Code should be unique per exam session!')

    def _compute_exams_count(self):
        for rec in self:
            rec.exams_count = len(rec.exam_ids)

    @api.constrains('start_date', 'end_date')
    def _check_date_time(self):
        if self.start_date > self.end_date:
            raise ValidationError(
                _('End Date cannot be set before Start Date.'))

    @api.onchange('course_id')
    def onchange_course(self):
        self.batch_id = False

    def act_draft(self):
        self.state = 'draft'

    def act_schedule(self):
        self.state = 'schedule'

    def act_held(self):
        self.state = 'held'

    def act_done(self):
        self.state = 'done'

    def act_cancel(self):
        self.state = 'cancel'

    def get_exam(self):
        return {
            'name': 'Exam ',
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'op.exam',
            'domain': [('id', 'in', self.exam_ids.ids)],
            'target': 'current',
        }
