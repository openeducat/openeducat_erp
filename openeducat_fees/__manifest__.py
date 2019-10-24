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
    'name': 'OpenEduCat Fees',
    'version': '13.0',
    'license': 'LGPL-3',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Manage Fees',
    'complexity': "easy",
    'author': 'Tech Receptives',
    'website': 'http://www.openeducat.org',
    'depends': ['openeducat_core', 'account'],
    'data': [
        'security/op_security.xml',
        'security/ir.model.access.csv',
        'report/report_menu.xml',
        'report/fees_analysis_report_view.xml',
        'wizard/fees_detail_report_wizard_view.xml',
        'views/fees_terms_view.xml',
        'views/student_view.xml',
        'views/course_view.xml',
        'menus/op_menu.xml',
    ],
    'images': [
        'static/description/openeducat_fees_banner.jpg',
    ],
    'demo': [
        'demo/product_category_demo.xml',
        'demo/product_demo.xml',
        'demo/fees_element_line_demo.xml',
        'demo/fees_terms_line_demo.xml',
        'demo/fees_terms_demo.xml',
        'demo/course_demo.xml',
        'demo/student_fees_details_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
