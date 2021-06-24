# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenEduCat Inc.
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
    'name': 'OpenEduCat Achievement',
    'version': '9.0.2.4.0',
    'license': 'LGPL-3',
    'category': 'Openerp Education',
    "sequence": 3,
    'summary': 'Manage Achievement',
    'complexity': "easy",
    'description': """
        This module adds the feature of achievement in Openeducat
    """,
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    'depends': ['openeducat_core'],
    'data': [
        'views/achievement_view.xml',
        'views/achievement_type_view.xml',
        'security/ir.model.access.csv',
        'achievement_menu.xml',
    ],
    'images': [
        'static/description/openeducat_achievement_banner.jpg',
    ],
    'demo': [
        'demo/achievement_type_demo.xml',
        'demo/achievement_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
