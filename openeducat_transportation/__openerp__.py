# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
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
    'name': 'OpenEduCat Transportation',
    'version': '9.0.2.4.0',
    'license': 'LGPL-3',
    'category': 'Openerp Education',
    "sequence": 3,
    'summary': 'Manage Transportations',
    'complexity': "easy",
    'description': """
        This module provide feature of Transportations.

    """,
    'author': 'Tech Receptives',
    'website': 'http://www.openeducat.org',
    'depends': ['openeducat_core'],
    'data': [
        'security/ir.model.access.csv',
        'views/stop_view.xml',
        'views/transportation_view.xml',
        'views/vehicle_view.xml',
        'transportation_menu.xml'
    ],
    'demo': [
        'demo/stop_demo.xml',
        'demo/vehicle_demo.xml',
        'demo/transportation_demo.xml',
    ],
    'images': [
        'static/description/openeducat_transportation_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
