###############################################################################
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
###############################################################################

from odoo import fields, models


class OpProgram(models.Model):
    _name = "op.program"
    _inherit = "mail.thread"
    _description = "openEMIS Program"

    name = fields.Char('Name', required=True, translate=True, tracking=True)
    code = fields.Char('Code', size=16, required=True, translate=True)
    max_unit_load = fields.Float("Maximum Unit Load")
    min_unit_load = fields.Float("Minimum Unit Load")
    department_id = fields.Many2one(
        'op.department', 'Department',
        default=lambda self:
        self.env.user.dept_id and self.env.user.dept_id.id or False)
    active = fields.Boolean(default=True)
    image_1920 = fields.Image('Image', attachment=True)
    program_level_id = fields.Many2one(
        'op.program.level', 'Program Level', required=True)


class OpProgramLevel(models.Model):
    _name = "op.program.level"
    _inherit = "mail.thread"
    _description = "openEMIS Program level"

    name = fields.Char('Name', required=True, translate=True, tracking=True)
