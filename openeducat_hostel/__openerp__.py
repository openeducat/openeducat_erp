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

{
    'name': 'OpenEduCat Hostel',
    'version': '9.0.2.4.0',
    'license': 'LGPL-3',
    'category': 'Openerp Education',
    "sequence": 3,
    'summary': 'Manage Hostels',
    'complexity': "easy",
    'description': """
        This module adds hostel management feature to OpenEduCat_Core.
    """,
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    'depends': ['openeducat_core', 'openeducat_facility'],
    'data': [
        'views/room_view.xml',
        'views/hostel_view.xml',
        'views/hostel_room_view.xml',
        'hostel_menu.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
        'demo/hostel_demo.xml',
        'demo/room_demo.xml',
        'demo/hostel_room_demo.xml',
    ],
    'images': [
        'static/description/openeducat_hostel_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
