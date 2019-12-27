# -*- coding: utf-8 -*-
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech Receptives(<http://www.techreceptives.com>).
#
##############################################################################

from odoo.tests import common


class TestClassroomCommon(common.SavepointCase):
    def setUp(self):
        super(TestClassroomCommon, self).setUp()
        self.op_classroom = self.env['op.classroom']
        self.op_asset = self.env['op.asset']
