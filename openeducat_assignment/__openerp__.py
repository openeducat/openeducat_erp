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
    'name': 'OpenEduCat Assignment',
    'version': '9.0.2.4.0',
    'license': 'LGPL-3',
    'category': 'Openerp Education',
    "sequence": 3,
    'summary': 'Manage Assgiments',
    'complexity': "easy",
    'description': """
        This module provide feature of Assignments.

    """,
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    'depends': ['openeducat_core'],
    'data': [
        'security/ir.model.access.csv',
        'views/assignment_view.xml',
        'views/assignment_type_view.xml',
        'views/assignment_sub_line_view.xml',
        'views/student_view.xml',
        'dashboard/assignment_faculty_dashboard.xml',
        'dashboard/assignment_student_dashboard.xml',
        'assignment_menu.xml'
    ],
    'demo': [
        'demo/assignment_type_demo.xml',
        'demo/assignment_demo.xml',
        'demo/assignment_sub_line_demo.xml'
    ],
    'images': [
        'static/description/openeducat_assignment_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
