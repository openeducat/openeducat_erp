###############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<https://www.openeducat.org>).
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

from .test_facility_common import TestFacilityCommon
from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo.tools import mute_logger

@tagged('post_install', '-at_install')
class TestFacilityModel(TestFacilityCommon):
    """Test cases for op.facility model"""

    def test_01_facility_creation(self):
        """Test basic facility creation"""
        facility = self.op_facility.create({
            'name': 'Projector',
            'code': 'PJ01',
        })
        self.assertEqual(facility.name, 'Projector')
        self.assertEqual(facility.code, 'PJ01')
        self.assertTrue(facility.active)

    def test_02_facility_unique_code(self):
        """Test unique constraint on facility code"""
        self.op_facility.create({
            'name': 'Facility 1',
            'code': 'UNIQUE01',
        })
        # Attempt to create another facility with same code
        with self.assertRaises(Exception), mute_logger('odoo.sql_db'):
            self.op_facility.create({
                'name': 'Facility 2',
                'code': 'UNIQUE01',
            })

    def test_03_facility_crud(self):
        """Test basic CRUD operations on facility"""
        facility = self.op_facility.create({
            'name': 'Old Name',
            'code': 'CRUD01',
        })
        # Update
        facility.write({'name': 'New Name'})
        self.assertEqual(facility.name, 'New Name')
        
        # Inactive
        facility.write({'active': False})
        self.assertFalse(facility.active)
        
        # Search
        search_res = self.op_facility.search([('code', '=', 'CRUD01'), ('active', '=', False)])
        self.assertIn(facility, search_res)


@tagged('post_install', '-at_install')
class TestFacilityLineModel(TestFacilityCommon):
    """Test cases for op.facility.line model"""

    def setUp(self):
        super(TestFacilityLineModel, self).setUp()
        self.test_facility = self.op_facility.create({
            'name': 'Test Facility Suite',
            'code': 'TFS01',
        })

    def test_01_line_creation(self):
        """Test basic facility line creation"""
        line = self.op_facility_line.create({
            'facility_id': self.test_facility.id,
            'quantity': 10.0,
        })
        self.assertEqual(line.facility_id.id, self.test_facility.id)
        self.assertEqual(line.quantity, 10.0)

    def test_02_line_quantity_validation(self):
        """Test quantity validation (must be > 0)"""
        # Test zero quantity
        with self.assertRaises(ValidationError):
            self.op_facility_line.create({
                'facility_id': self.test_facility.id,
                'quantity': 0.0,
            })
        # Test negative quantity
        with self.assertRaises(ValidationError):
            self.op_facility_line.create({
                'facility_id': self.test_facility.id,
                'quantity': -5.0,
            })

    def test_03_line_multiple(self):
        """Test creating multiple facility lines"""
        facility2 = self.op_facility.create({
            'name': 'Second Facility',
            'code': 'SF02',
        })
        line1 = self.op_facility_line.create({
            'facility_id': self.test_facility.id,
            'quantity': 5.0,
        })
        line2 = self.op_facility_line.create({
            'facility_id': facility2.id,
            'quantity': 3.0,
        })
        self.assertTrue(line1)
        self.assertTrue(line2)
        self.assertNotEqual(line1.id, line2.id)
