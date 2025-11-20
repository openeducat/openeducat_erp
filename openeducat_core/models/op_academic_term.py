# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<https://www.openeducat.org>).
#
##############################################################################

from odoo import fields, models


class OpAcademicTerm(models.Model):

    _name = 'op.academic.term'
    _description = "Academic Term"

    name = fields.Char('Name', required=True)
    term_start_date = fields.Date('Start Date', required=True)
    term_end_date = fields.Date('End Date', required=True)
    academic_year_id = fields.Many2one(
        'op.academic.year', 'Academic Year', required=True)
    parent_term = fields.Many2one('op.academic.term', 'Parent Term')
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.user.company_id)

    _unique_name = models.Constraint('UNIQUE(name)', 'Name must be unique.')
    _unique_start_date = models.Constraint('UNIQUE(term_start_date)',
                                           'Start date must be unique.')
    _unique_end_date = models.Constraint('UNIQUE(term_end_date)',
                                         'End date must be unique.')
