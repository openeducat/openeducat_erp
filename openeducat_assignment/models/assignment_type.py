# Part of openEMIS. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    openEMIS
#    Copyright (C) 2009-TODAY openEMIS(<https://www.openemis.org>).
#
##############################################################################

from odoo import fields, models


class GradingAssigmentType(models.Model):
    _name = 'grading.assignment.type'
    _description = "Assignment Type"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code")
    assign_type = fields.Selection([('sub', 'Subjective'),
                                    ('attendance', 'Attendance')],
                                   string='Type', default='sub')
