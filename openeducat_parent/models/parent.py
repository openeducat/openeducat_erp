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


class OpParent(models.Model):
    _name = "op.parent"
    _description = "Parent"

    name = fields.Many2one('res.partner', 'Name', required=True,
                           domain="[('is_parent', '=', True)]")
    user_id = fields.Many2one('res.users', string='User', store=True)
    student_ids = fields.Many2many('op.student', string='Student(s)', required=True,)
    mobile = fields.Char(string='Mobile')
    email = fields.Char(string='Email')
    active = fields.Boolean(default=True)
    relationship_id = fields.Many2one('op.parent.relationship',
                                      'Relation with Student', required=True)

    _unique_parent = models.Constraint('unique(name)',
                                       'Can not create parent multiple times.!')

    @api.onchange('name')
    def _onchange_name(self):
        if self.name:
            self.user_id = self.name.user_id.id if self.name.user_id else False
            self.mobile = self.name.phone
            self.email = self.name.email

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            partner_id = vals.get('name')
            parent_email = vals.get('email')
            parent_mobile = vals.get('mobile')

            if isinstance(partner_id, int):
                partner = self.env['res.partner'].browse(partner_id)
                if partner.exists():
                    update_vals = {'is_parent': True}
                    if parent_email and not partner.email:
                        update_vals['email'] = parent_email
                    if parent_mobile and not partner.phone:
                        update_vals['phone'] = parent_mobile
                    partner.write(update_vals)
                    continue

            parent_name = vals.get('name')
            partner = self.env['res.partner'].search([
                '|', '|',
                ('name', '=', parent_name),
                ('email', '=', parent_email),
                ('phone', '=', parent_mobile),
            ], limit=1)

            if partner:
                update_vals = {'is_parent': True}
                if parent_email and not partner.email:
                    update_vals['email'] = parent_email
                if parent_mobile and not partner.phone:
                    update_vals['phone'] = parent_mobile
                partner.write(update_vals)

                vals['name'] = partner.id
            else:
                new_partner = self.env['res.partner'].create({
                    'name': parent_name,
                    'email': parent_email,
                    'phone': parent_mobile,
                    'is_parent': True,
                })
                vals['name'] = new_partner.id
                vals['email'] = parent_email
                vals['phone'] = parent_mobile

        res = super(OpParent, self).create(vals_list)

        for record in res:
            if record.student_ids and record.name.user_id:
                user_ids = [s.user_id.id for s in record.student_ids if s.user_id]
                record.user_id.child_ids = [(6, 0, user_ids)]

            if record.name and not record.name.is_parent:
                record.name.is_parent = True

        return res

    def write(self, vals):
        for rec in self:
            res = super(OpParent, self).write(vals)
            if vals.get('student_ids', False) and rec.name.user_id:
                student_ids = rec.student_ids.browse(rec.student_ids.ids)
                usr_ids = [student_id.user_id.id for student_id in student_ids
                           if student_id.user_id]
                rec.user_id.child_ids = [(6, 0, usr_ids)]
            rec.env.registry.clear_cache()
            return res

    def unlink(self):
        for record in self:
            if record.name.user_id:
                record.user_id.child_ids = [(6, 0, [])]
            return super(OpParent, self).unlink()

    def create_parent_user(self):
        template = self.env.ref('openeducat_parent.parent_template_user')
        users_res = self.env['res.users']
        for record in self:
            partner = record.name
            if not (partner.email or record.email):
                raise ValidationError(_('Update parent email id first.'))
            if not partner.email:
                partner.email = record.email
            if not partner.phone and record.mobile:
                partner.phone = record.mobile

            if not record.name.user_id:
                groups_id = template and template.group_ids or False
                user_ids = [
                    parent.user_id.id for
                    parent in record.student_ids if parent.user_id]
                user_id = users_res.create({
                    'name': record.name.name,
                    'partner_id': record.name.id,
                    'login': record.name.email or record.email,
                    'is_parent': True,
                    'tz': self.env.context.get('tz'),
                    'group_ids': groups_id,
                    'child_ids': [(6, 0, user_ids)]
                })
                record.user_id = user_id
                record.name.user_id = user_id

    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Parent'),
            'template': '/openeducat_parent/static/xls/op_parent.xls'
        }]


class OpStudent(models.Model):
    _inherit = "op.student"

    parent_ids = fields.Many2many('op.parent', string='Parent')

    @api.model_create_multi
    def create(self, vals):
        res = super(OpStudent, self).create(vals)
        for values in vals:
            if values.get('parent_ids', False):
                for parent_id in res.parent_ids:
                    if parent_id.user_id:
                        user_ids = [student.user_id.id for student
                                    in parent_id.student_ids if student.user_id]
                        parent_id.user_id.child_ids = [(6, 0, user_ids)]
        return res

    def write(self, vals):
        res = super(OpStudent, self).write(vals)
        if vals.get('parent_ids', False):
            user_ids = []
            if self.parent_ids:
                for parent in self.parent_ids:
                    if parent.user_id:
                        user_ids = [parent.user_id.id for parent in parent.student_ids
                                    if parent.user_id]
                        parent.user_id.child_ids = [(6, 0, user_ids)]
            else:
                user_ids = self.env['res.users'].search([
                    ('child_ids', 'in', self.user_id.id)])
                for user_id in user_ids:
                    child_ids = user_id.child_ids.ids
                    child_ids.remove(self.user_id.id)
                    user_id.child_ids = [(6, 0, child_ids)]
        if vals.get('user_id', False):
            for parent_id in self.parent_ids:
                child_ids = parent_id.user_id.child_ids.ids
                child_ids.append(vals['user_id'])
                parent_id.name.user_id.child_ids = [(6, 0, child_ids)]
        self.env.registry.clear_cache()
        return res

    def unlink(self):
        for record in self:
            if record.parent_ids:
                for parent_id in record.parent_ids:
                    child_ids = parent_id.user_id.child_ids.ids
                    child_ids.remove(record.user_id.id)
                    parent_id.name.user_id.child_ids = [(6, 0, child_ids)]
        return super(OpStudent, self).unlink()

    def get_parent(self):
        self.ensure_one()
        action = self.env.ref(
            'openeducat_parent.act_open_op_parent_view').sudo().read()[0]
        action['domain'] = [('student_ids', 'in', self.ids)]
        action['context'] = {'default_student_ids': [(6, 0, self.ids)]}
        return action


class OpSubjectRegistration(models.Model):
    _inherit = "op.subject.registration"

    @api.model_create_multi
    def create(self, vals):
        if self.env.user.child_ids:
            raise ValidationError(_('Invalid Action!\n Parent can not \
            create Subject Registration!'))
        return super(OpSubjectRegistration, self).create(vals)

    def write(self, vals):
        if self.env.user.child_ids:
            raise ValidationError(_('Invalid Action!\n Parent can not edit \
            Subject Registration!'))
        return super(OpSubjectRegistration, self).write(vals)
