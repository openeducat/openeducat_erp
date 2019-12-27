# -*- coding: utf-8 -*-
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech Receptives(<http://www.techreceptives.com>).
#
##############################################################################

from odoo.tests import common


class TestActivityCommon(common.SavepointCase):
    def setUp(self):
        super(TestActivityCommon, self).setUp()
        self.op_activity_type = self.env['op.activity.type']
        self.op_activity = self.env['op.activity']
        self.op_student_migrate_wizard = self.env['student.migrate']
