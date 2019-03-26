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
    'name': 'OpenEduCat Timetable',
    'version': '12.0',
    'license': 'LGPL-3',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Manage TimeTables',
    'complexity': "easy",
    'author': 'Tech Receptives',
    'website': 'http://www.openeducat.org',
    'depends': ['openeducat_classroom'],
    'data': [
        'security/op_security.xml',
        'security/ir.model.access.csv',
        'views/timetable_view.xml',
        'views/timing_view.xml',
        'views/faculty_view.xml',
        'report/report_timetable_student_generate.xml',
        'report/report_timetable_teacher_generate.xml',
        'report/report_menu.xml',
        'wizard/generate_timetable_view.xml',
        'wizard/time_table_report.xml',
        'wizard/session_confirmation.xml',
        'views/timetable_templates.xml',
        'menus/op_menu.xml',
    ],
    'demo': [
        'demo/timing_demo.xml',
        'demo/op_timetable_demo.xml'
    ],
    'test': [
        'test/timetable_sub_value.yml',
        'test/generate_timetable.yml'
    ],
    'images': [
        'static/description/openeducat_timetable_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
