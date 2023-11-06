# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
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
            for rec in record.facilities:
                info('      facilities : %s' % rec.facility_id.name)
            for rec1 in record.asset_line:
                info('      asset_line : %s' % rec1.product_id.name)
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
            'asset_id': self.env.ref('openeducat_classroom.op_classroom_1').id,
            'product_id': product.id,
            'code': 1,
            'product_uom_qty': 11
        })
        for record in assets:
            info('      Asset Name: %s' % record.asset_id.name)
            info('      Product Name : %s' % record.product_id.name)
            info('      Product Quantity : %s' % record.product_uom_qty)
