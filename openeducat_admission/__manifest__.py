# -*- coding: utf-8 -*-
##############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech Receptives(<http://www.techreceptives.com>).
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
##############################################################################

{
    'name': "OpenEduCat Admission",
    'version': '10.0.3.0.0',
    'license': 'LGPL-3',
    'category': 'Education',
    'sequence': 3,
    'summary': "Manage Admissions""",
    'complexity': "easy",
    'author': 'Tech Receptives',
    'website': 'http://www.openeducat.org',
    'depends': ['openeducat_fees', 'openeducat_core'],
    'data': [
        'views/admission_register_view.xml',
        'views/admission_view.xml',
        'views/admission_sequence.xml',
        'views/student_view.xml',
        'report/report_menu.xml',
        'report/report_admission_analysis.xml',
        'wizard/admission_analysis_wizard_view.xml',
        'admission_menu.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
        'demo/product_category_demo.xml',
        'demo/product_demo.xml',
        'demo/admission_register_demo.xml',
        'demo/admission_demo.xml',
        'demo/student_fees_details_demo.xml',
    ],
    'test': [
        'test/res_users_creation.yml',
        'test/batch_course_fees.yml',
        'test/admission_register_creation.yml',
    ],
    'images': [
        'static/description/openeducat_admission_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
