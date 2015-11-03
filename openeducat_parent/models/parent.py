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

from openerp import models, fields


class OpParent(models.Model):
    _name = 'op.parent'

    name = fields.Many2one(
        'res.partner', 'Name', default=lambda self: self.env[
            'res.partner'].search([('user_id', '=', self.env.uid)]),
        required=True)
    student_ids = fields.Many2many('op.student', string='Student(s)')
    user_id = fields.Many2one(
        'res.users', 'User', default=lambda self: self.env.uid, required=True)


class OpStudent(models.Model):

    _inherit = 'op.student'

    parent_ids = fields.Many2many('op.parent', string='Parent')


class ResUsers(models.Model):
    _inherit = "res.users"

    parent_ids = fields.One2many('op.parent', 'user_id', 'Parents')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
