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
    'name': 'OpenEduCat Attendance',
    'version': '9.0.2.4.0',
    'license': 'LGPL-3',
    'category': 'Openerp Education',
    "sequence": 3,
    'summary': 'Manage Attendances',
    'complexity': "easy",
    'description': """
        This module provide feature of Attendance Management.

    """,
    'author': 'Tech Receptives',
    'website': 'http://www.openeducat.org',
    'depends': ['openeducat_core'],
    'data': [
        'security/ir.model.access.csv',
        'views/attendance_register_view.xml',
        'views/attendance_sheet_view.xml',
        'views/attendance_line_view.xml',
        'wizards/attendance_import_view.xml',
        'wizards/student_attendance_wizard_view.xml',
        'report/student_attendance_report.xml',
        'report/report_menu.xml',
        'attendance_menu.xml'
    ],
    'demo': [
        'demo/attendance_register_demo.xml',
        'demo/attendance_sheet_demo.xml',
        'demo/attendance_line_demo.xml',
    ],
    'images': [
        'static/description/openeducat_attendance_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
