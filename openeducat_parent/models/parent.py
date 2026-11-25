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
            # the contact's own login, not its salesperson (partner.user_id)
            self.user_id = self.name.user_ids[:1]
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

        res._update_parent_user_children()
        for record in res:
            if record.name and not record.name.is_parent:
                record.name.is_parent = True

        return res

    def _update_parent_user_children(self):
        """Give each parent login (op.parent.user_id) its students' logins
        as child_ids. The portal rules of the parent read child_ids.

        Note: partner.user_id is the contact's salesperson, not the
        parent's login, so it must not be used here.
        """
        for rec in self:
            if rec.user_id:
                rec.user_id.child_ids = [(6, 0, rec.student_ids.user_id.ids)]

    def write(self, vals):
        old_users = self.user_id if 'user_id' in vals else self.env['res.users']
        res = super(OpParent, self).write(vals)
        # a login unlinked from the parent loses the children it got from it
        (old_users - self.user_id).write({'child_ids': [(5, 0, 0)]})
        if 'student_ids' in vals or 'user_id' in vals:
            self._update_parent_user_children()
        return res

    def unlink(self):
        self.user_id.write({'child_ids': [(5, 0, 0)]})
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

            if not record.user_id and record.name.user_ids:
                # the contact already has a login: link it
                record.user_id = record.name.user_ids[:1]
            if not record.user_id:
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
            record._update_parent_user_children()

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
        res.parent_ids._update_parent_user_children()
        return res

    def write(self, vals):
        # parents the students had before the write lose them if unlinked
        parents = self.parent_ids if 'parent_ids' in vals else self.env['op.parent']
        res = super(OpStudent, self).write(vals)
        if 'parent_ids' in vals or 'user_id' in vals:
            # recomputed from the students' logins: a changed student login
            # replaces the old one on the parent login
            (parents | self.parent_ids)._update_parent_user_children()
        return res

    def unlink(self):
        parents = self.parent_ids
        res = super(OpStudent, self).unlink()
        parents.exists()._update_parent_user_children()
        return res

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
        _read_only_fields = {'is_read_by_parent', 'is_read'}
        if self.env.user.child_ids and not set(vals.keys()) <= _read_only_fields:
            raise ValidationError(_('Invalid Action!\n Parent can not edit '
                                    'Subject Registration!'))
        return super(OpSubjectRegistration, self).write(vals)
