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
    'name': 'OpenEduCat Scholarship',
    'version': '2.4.0',
    'category': 'Openerp Education',
    "sequence": 3,
    'summary': 'Manage Scholarship',
    'complexity': "easy",
    'description': """
        This module adds the feature of scholarship in Openeducat
    """,
    'author': 'Tech Receptives',
    'website': 'http://www.openeducat.org',
    'depends': ['openeducat_core'],
    'data': [
        'views/scholarship_view.xml',
        'views/scholarship_type_view.xml',
        'security/ir.model.access.csv',
        'scholarship_menu.xml',
    ],
    'demo': [
        'demo/op.scholarship.type.csv',
        'demo/op.scholarship.csv',
    ],
    'images': [
        'static/description/openeducat_scholarship_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
