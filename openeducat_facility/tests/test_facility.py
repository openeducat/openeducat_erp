# -*- coding: utf-8 -*-
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


class TestFacilityLine(TestFacilityCommon):

    def setUp(self):
        super(TestFacilityLine, self).setUp()

    def test_case_facility_line(self):

        types = self.op_facility_line.create({
            'facility_id': self.env.ref
            ('openeducat_facility.op_facility_1').id,
            'quantity': '1.0',
        })
        for facility in types:
            facility.check_quantity()
