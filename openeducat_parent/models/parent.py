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
from odoo.exceptions import Warning


class OpParent(models.Model):
    _name = 'op.parent'

    name = fields.Many2one(
        'res.partner', 'Name', default=lambda self: self.env[
            'res.partner'].search([('user_id', '=', self.env.uid)]),
        required=True)
    student_ids = fields.Many2many('op.student', string='Student(s)')
    user_id = fields.Many2one(
        'res.users', 'User', default=lambda self: self.env.uid, required=True)

    @api.model
    def create(self, vals):
        res = super(OpParent, self).create(vals)
        if vals.get('student_ids', False):
            student_ids = self.student_ids.browse(res.student_ids.ids)
            user_ids = [student_id.user_id.id for student_id in student_ids
                        if student_id.user_id]
            res.user_id.child_ids = [(6, 0, user_ids)]
        return res

    @api.multi
    def write(self, vals):
        res = super(OpParent, self).write(vals)
        if vals.get('student_ids', False):
            student_ids = self.student_ids.browse(self.student_ids.ids)
            user_ids = [student_id.user_id.id for student_id in student_ids
                        if student_id.user_id]
            self.user_id.child_ids = [(6, 0, user_ids)]
        self.clear_caches()
        return res

    @api.multi
    def unlink(self):
        self.user_id.child_ids = [(6, 0, [])]
        return super(OpParent, self).unlink()


class OpStudent(models.Model):

    _inherit = 'op.student'

    parent_ids = fields.Many2many('op.parent', string='Parent')

    @api.model
    def create(self, vals):
        res = super(OpStudent, self).create(vals)
        if vals.get('parent_ids', False):
            for parent_id in res.parent_ids:
                user_ids = [student_id.user_id.id for student_id in
                            parent_id.student_ids if student_id.user_id]
                parent_id.user_id.child_ids = [(6, 0, user_ids)]
        return res

    @api.multi
    def write(self, vals):
        res = super(OpStudent, self).write(vals)
        if vals.get('parent_ids', False):
            user_ids = []
            if self.parent_ids:
                for parent_id in self.parent_ids:
                    user_ids = [student_id.user_id.id for student_id in
                                parent_id.student_ids if student_id.user_id]
                    parent_id.user_id.child_ids = [(6, 0, user_ids)]
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
                parent_id.user_id.child_ids = [(6, 0, child_ids)]
        self.clear_caches()
        return res

    @api.multi
    def unlink(self):
        if self.parent_ids:
            for parent_id in self.parent_ids:
                child_ids = parent_id.user_id.child_ids.ids
                child_ids.remove(self.user_id.id)
                parent_id.user_id.child_ids = [(6, 0, child_ids)]
        return super(OpStudent, self).unlink()


class OpSubjectRegistration(models.Model):
    _inherit = 'op.subject.registration'

    @api.model
    def create(self, vals):
        if self.env.user.child_ids:
            raise Warning(_('Invalid Action!\n Parent can not \
            create Subject Registration!'))
        return super(OpSubjectRegistration, self).create(vals)

    @api.multi
    def write(self, vals):
        if self.env.user.child_ids:
            raise Warning(_('Invalid Action!\n Parent can not edit \
            Subject Registration!'))
        return super(OpSubjectRegistration, self).write(vals)


# class ResUsers(models.Model):
#     _inherit = "res.users"

#     parent_ids = fields.One2many('op.parent', 'user_id', 'Parents')
