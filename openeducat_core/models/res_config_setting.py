# -*- coding: utf-8 -*-
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech Receptives(<http://www.techreceptives.com>).
#
##############################################################################

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_openeducat_activity = fields.Boolean(string="Activity")
    module_openeducat_facility = fields.Boolean(string="Facility")
    module_openeducat_parent = fields.Boolean(string="Parent")
    module_openeducat_assignment = fields.Boolean(string="Assignment")
    module_openeducat_classroom = fields.Boolean(string="Classroom")
    module_openeducat_fees = fields.Boolean(string="Fees")
    module_openeducat_admission = fields.Boolean(string="Admission")
    module_openeducat_timetable = fields.Boolean(string="Timetable")
    module_openeducat_exam = fields.Boolean(string="Exam")
    module_openeducat_library = fields.Boolean(string="Library")
    module_openeducat_attendance = fields.Boolean(string="Attendance")
