# -*- coding: utf-8 -*-
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech Receptives(<http://www.techreceptives.com>).
#
##############################################################################
from logging import info
from .test_classroom_common import TestClassroomCommon


class TestClassroom(TestClassroomCommon):

    def setUp(self):
        super(TestClassroom, self).setUp()

    def test_case_classroom_1(self):
        classroom = self.op_classroom.search([])
        if not classroom:
            raise AssertionError(
                'Error in data, please check for reference Classroom')
        for record in classroom:
            info('      Class Name: %s' % record.name)
            info('      Code : %s' % record.code)
            info('      Course Name : %s' % record.course_id.name)
            info('      Capacity : %s' % record.capacity)
            info('      facilities : %s' % record.facilities)
            info('      asset_line : %s' % record.asset_line.product_id)
            record.onchange_course()


class TestAsset(TestClassroomCommon):

    def setUp(self):
        super(TestAsset, self).setUp()

    def test_case_1_asset(self):
        product = self.env['product.product'].create({
            'default_code': 'FIFO',
            'name': 'Chairs',
            'categ_id': self.env.ref('product.product_category_1').id,
            'list_price': 100.0,
            'standard_price': 70.0,
            'uom_id': self.env.ref('uom.product_uom_kgm').id,
            'uom_po_id': self.env.ref('uom.product_uom_kgm').id,
            'description': 'FIFO Ice Cream',
        })
        assets = self.op_asset.create({
            'product_id': product.id,
            'code': 1,
            'product_uom_qty': 11
        })
        for record in assets:
            info('      Asset Name: %s' % record.asset_id.name)
            info('      Product Name : %s' % record.product_id.name)
            info('      Product Quantity : %s' % record.product_uom_qty)
