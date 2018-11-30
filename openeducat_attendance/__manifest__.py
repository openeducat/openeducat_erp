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
    'version': '12.0',
    'license': 'LGPL-3',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Manage Attendances',
    'complexity': "easy",
    'author': 'Tech Receptives',
    'website': 'http://www.openeducat.org',
    'depends': ['openeducat_timetable'],
    'data': [
        'security/op_security.xml',
        'security/ir.model.access.csv',
        'wizards/attendance_import_view.xml',
        'wizards/student_attendance_wizard_view.xml',
        'views/attendance_register_view.xml',
        'views/attendance_sheet_view.xml',
        'views/attendance_line_view.xml',
        'report/student_attendance_report.xml',
        'report/report_menu.xml',
        'menus/op_menu.xml'
    ],
    'test': [
        'test/res_users_test.yml',
        'test/attendance_sub_value_test.yml',
        'test/attendance_process_test.yml'
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
