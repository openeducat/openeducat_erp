# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<https://www.openeducat.org>).
#
##############################################################################

from odoo import fields, models


class GradingAssigmentType(models.Model):
    _name = 'grading.assignment.type'
    _description = "Assignment Type"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    assign_type = fields.Selection([('sub', 'Subjective'),
                                    ('attendance', 'Attendance')],
                                   string='Type', default='sub')

    _unique_code = models.Constraint(
        'unique(code)', "The code must be unique across all assignment types.")
