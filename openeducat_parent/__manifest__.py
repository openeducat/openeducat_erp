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
    'name': 'OpenEduCat Parent',
    'version': '13.0',
    'license': 'LGPL-3',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Manage Parent',
    'complexity': "easy",
    'author': 'Tech Receptives',
    'website': 'http://www.openeducat.org',
    'depends': ['openeducat_core'],
    'data': [
        'security/op_security.xml',
        'security/ir.model.access.csv',
        'data/parent_user_data.xml',
        'views/parent_view.xml',
        'menus/op_menu.xml',
    ],
    'demo': [
        'demo/res_partner_demo.xml',
        'demo/res_users_demo.xml',
        'demo/parent_demo.xml',
    ],
    'images': [
        'static/description/openeducat_parent_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
