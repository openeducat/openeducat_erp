# -*- coding: utf-8 -*-
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech Receptives(<http://www.techreceptives.com>).
#
##############################################################################

from odoo.tests import common


class TestAssignmentCommon(common.SavepointCase):
    def setUp(self):
        super(TestAssignmentCommon, self).setUp()
        self.op_assignment = self.env['op.assignment']
        self.op_assignment_subline = self.env['op.assignment.sub.line']
