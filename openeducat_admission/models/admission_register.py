##############################################################################
#
#    openEMIS
#    Copyright (C) 2009-TODAY openEMIS(<https://www.openemis.org>).
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
##############################################################################

from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class OpAdmissionRegister(models.Model):
    _name = "op.admission.register"
    _inherit = "mail.thread"
    _description = "Admission Register"
    _order = 'id DESC'

    name = fields.Char(
        'Name', required=True, readonly=True)
    start_date = fields.Date(
        'Start Date', required=True, readonly=True,
        default=fields.Date.today())
    end_date = fields.Date(
        'End Date', required=False, readonly=True,
        default=(fields.Date.today() + relativedelta(days=30)))
    course_id = fields.Many2one(
        'op.course', 'Course', readonly=True, tracking=True)
    min_count = fields.Integer(
        'Minimum No. of Admission', readonly=True)
    max_count = fields.Integer(
        'Maximum No. of Admission', readonly=True, default=30)
    product_id = fields.Many2one(
        'product.product', 'Course Fees',
        domain=[('type', '=', 'service')], tracking=True)
    admission_ids = fields.One2many(
        'op.admission', 'register_id', 'Admissions')
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirmed'),
         ('cancel', 'Cancelled'), ('application', 'Application Gathering'),
         ('admission', 'Admission Process'), ('done', 'Done')],
        'Status', default='draft', tracking=True)
    active = fields.Boolean(default=True)

    academic_years_id = \
        fields.Many2one('op.academic.year',
                        'Academic Year', readonly=True,
                        tracking=True)
    academic_term_id = fields.Many2one('op.academic.term',
                                       'Terms', readonly=True,
                                       tracking=True)
    minimum_age_criteria = fields.Integer('Minimum Required Age(Years)', default=3)
    application_count = fields.Integer(string="Total_record",
                                       compute="_compute_calculate_record_application")
    is_favorite = fields.Boolean(string="Is Favorite", default=False)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.user.company_id)
    draft_count = fields.Integer(compute="_compute_counts")
    confirm_count = fields.Integer(compute="_compute_counts")
    done_count = fields.Integer(compute="_compute_counts")
    online_count = fields.Integer(compute='_compute_application_counts')
    admission_base = fields.Selection([('program', 'Program'), ('course', 'Course')],
                                      default='course')
    admission_fees_line_ids = fields.One2many('op.admission.fees.line', 'register_id',
                                              string='Admission Fees Configuration')

    @api.onchange('admission_base')
    def onchange_admission_base(self):
        if self.admission_base:
            if self.admission_base == 'program':
                self.course_id = None
                self.product_id = None
            else:
                self.program_id = None
                self.admission_fees_line_ids = None

    program_id = fields.Many2one('op.program', string="Program", tracking=True)

    def _compute_counts(self):
        for record in self:
            draft_admissions = record.admission_ids.filtered(
                lambda a: a.state == 'draft')
            confirmed_admissions = record.admission_ids.filtered(
                lambda a: a.state == 'confirm')
            done_admissions = record.admission_ids.filtered(
                lambda a: a.state == 'done')

            record.draft_count = len(draft_admissions)
            record.confirm_count = len(confirmed_admissions)
            record.done_count = len(done_admissions)

    def _compute_application_counts(self):
        for record in self:
            record.draft_count = record.admission_ids.filtered(
                lambda a: a.state == 'draft').mapped('id').__len__()
            record.online_count = record.admission_ids.filtered(
                lambda a: a.state == 'online').mapped('id').__len__()

    @api.constrains('start_date', 'end_date')
    def check_dates(self):
        for record in self:
            start_date = fields.Date.from_string(record.start_date)
            end_date = fields.Date.from_string(record.end_date)
            if end_date and start_date > end_date:
                raise ValidationError(
                    _("End Date cannot be set before Start Date."))

    @api.constrains('min_count', 'max_count')
    def check_no_of_admission(self):
        for record in self:
            if (record.min_count <= 0) or (record.max_count <= 0):
                raise ValidationError(
                    _("No of Admission should be positive!"))
            if record.min_count > record.max_count:
                raise ValidationError(_(
                    "Min Admission can't be greater than Max Admission"))

    def open_student_application(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "op.admission",
            "domain": [("register_id", "=", self.id)],
            "name": "Applications",
            "view_mode": "list,form",
        }

    def _compute_calculate_record_application(self):
        record = self.env["op.admission"].search_count([
            ("register_id", "=", self.id)])
        self.application_count = record

    def confirm_register(self):
        self.state = 'confirm'

    def set_to_draft(self):
        self.state = 'draft'

    def cancel_register(self):
        self.state = 'cancel'

    def start_application(self):
        self.state = 'application'

    def start_admission(self):
        self.state = 'admission'

    def close_register(self):
        self.state = 'done'

    def action_open_draft_courses(self):
        return {
            'name': 'Draft Admissions',
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'op.admission',
            'domain': [
                ('id', 'in', self.admission_ids.ids),
                ('state', '=', 'draft'),
            ],
            'target': 'current',
        }

    def action_open_confirmed_courses(self):
        return {
            'name': 'Confirmed Courses',
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'op.admission',
            'domain': [('id', 'in', self.admission_ids.ids), ('state', '=', 'confirm')],
            'target': 'current',
        }

    def action_open_enrolled_courses(self):
        return {
            'name': 'Enrolled Courses',
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'op.admission',
            'domain': [('id', 'in', self.admission_ids.ids), ('state', '=', 'done')],
            'target': 'current',
        }

    def action_open_online_courses(self):
        return {
            'name': 'Enrolled Courses',
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'op.admission',
            'domain': [('id', 'in', self.admission_ids.ids), ('state', '=', 'online')],
            'target': 'current',
        }


class AdmissionRegisterFeesLine(models.Model):
    _name = 'op.admission.fees.line'
    _description = "Admission Fees Line"

    course_id = fields.Many2one('op.course', string="Course", required=True)
    course_fees_product_id = fields.Many2one('product.product', string="Course Fees")
    register_id = fields.Many2one('op.admission.register', string="Admission Register")
