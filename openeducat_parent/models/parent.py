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
    student_ids = fields.Many2many('op.student', string='Student(s)', required=True, )
    mobile = fields.Char(string='Mobile')
    email = fields.Char(string='Email')
    active = fields.Boolean(default=True)
    relationship_id = fields.Many2one('op.parent.relationship',
                                      'Relation with Student', required=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company,
        index=True)

    _unique_parent = models.Constraint('unique(name)',
                                       'Can not create parent multiple times.!')

    @api.onchange('name')
    def _onchange_name(self):
        if self.name:
            # the contact's own login, not partner.user_id (its salesperson)
            self.user_id = self.name.user_ids[:1]
            self.mobile = self.name.phone
            self.email = self.name.email

    def _sync_children(self):
        """Make the parent login's child_ids match the logins of its students."""
        # Skip entirely when none of the parents have a login: there is
        # nothing to write on res.users, and no cache to invalidate.
        touched_users = self.mapped('user_id')
        if not touched_users:
            return
        for rec in self:
            if rec.user_id:
                rec.user_id.sudo().child_ids = [
                    (6, 0, rec.student_ids.user_id.ids)]
        # Targeted cache invalidation: only the child_ids field on the users
        # we actually wrote to, so bulk operations stay cheap.
        touched_users.invalidate_recordset(['child_ids'])

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
            if record.name and not record.name.is_parent:
                record.name.is_parent = True

        res._sync_children()
        return res

    def write(self, vals):
        old_users = self.user_id if 'user_id' in vals else self.env['res.users']
        res = super(OpParent, self).write(vals)
        if 'student_ids' in vals or 'user_id' in vals:
            # a login that is no longer this parent's loses its children
            dropped = old_users - self.user_id
            if dropped:
                dropped.sudo().write({'child_ids': [(5, 0, 0)]})
            self._sync_children()
        if 'active' in vals:
            # Cascade archive/unarchive to the parent's login, so an archived
            # parent cannot keep signing in and seeing the (former) children.
            touched_users = self.env['res.users']
            for rec in self:
                if not rec.user_id:
                    continue
                touched_users |= rec.user_id
                if vals['active']:
                    rec.user_id.sudo().write({
                        'active': True,
                        'child_ids': [(6, 0, rec.student_ids.user_id.ids)],
                    })
                else:
                    rec.user_id.sudo().write({
                        'active': False,
                        'child_ids': [(6, 0, [])],
                    })
            if touched_users:
                # Targeted: only the fields we wrote, only the records we wrote.
                touched_users.invalidate_recordset(['active', 'child_ids'])
        return res

    def unlink(self):
        for record in self:
            if record.user_id:
                record.user_id.sudo().child_ids = [(6, 0, [])]
        return super(OpParent, self).unlink()

    def create_parent_user(self):
        template = self.env.ref('openeducat_parent.parent_template_user')
        users_res = self.env['res.users'].sudo()
        for record in self:
            partner = record.name
            if not (partner.email or record.email):
                raise ValidationError(_('Update parent email id first.'))
            if not partner.email:
                partner.email = record.email
            if not partner.phone and record.mobile:
                partner.phone = record.mobile

            # partner.user_id is the contact's salesperson; the parent's
            # login is the user whose partner is this contact
            user = record.user_id or partner.sudo().user_ids[:1]
            if not user:
                groups_id = template and template.group_ids or False
                user = users_res.create({
                    'name': partner.name,
                    'partner_id': partner.id,
                    'login': partner.email or record.email,
                    'is_parent': True,
                    'tz': self.env.context.get('tz'),
                    'group_ids': groups_id,
                })
            if record.user_id != user:
                record.user_id = user  # write() syncs the children
            else:
                record._sync_children()

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
        res.parent_ids._sync_children()
        return res

    def write(self, vals):
        track = 'parent_ids' in vals or 'user_id' in vals
        old_parents = self.parent_ids if track else self.env['op.parent']
        res = super(OpStudent, self).write(vals)
        if track:
            # Re-sync parents the student left and parents it now has, so a
            # new / changed / removed student login reaches the parent LOGIN.
            (old_parents | self.parent_ids)._sync_children()
        return res

    def unlink(self):
        parents = self.parent_ids
        res = super(OpStudent, self).unlink()
        parents.exists()._sync_children()
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