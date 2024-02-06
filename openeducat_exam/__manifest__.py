# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<https://www.openeducat.org>).
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
    'name': 'OpenEduCat Exam',
    'version': '17.0.1.0',
    'license': 'LGPL-3',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Manage Exam',
    'complexity': "easy",
    'author': 'OpenEduCat Inc',
    'website': 'https://www.openeducat.org',
    'depends': ['openeducat_classroom'],
    'data': [
        'security/op_security.xml',
        'security/ir.model.access.csv',
        'views/res_partner_view.xml',
        'views/exam_attendees_view.xml',
        'views/exam_room_view.xml',
        'views/exam_session_view.xml',
        'views/exam_type_view.xml',
        'wizard/room_distribution_view.xml',
        'wizard/held_exam_view.xml',
        'views/exam_view.xml',
        'views/marksheet_line_view.xml',
        'views/marksheet_register_view.xml',
        'views/grade_configuration_view.xml',
        'views/result_line_view.xml',
        'views/result_template_view.xml',
        'report/report_ticket.xml',
        'report/student_marksheet.xml',
        'report/report_menu.xml',
        'wizard/student_hall_tickets_wizard_view.xml',
        'menus/op_menu.xml',
    ],
    'demo': [
        'demo/exam_room_demo.xml',
        'demo/exam_type_demo.xml',
        'demo/exam_session_demo.xml',
        'demo/exam_demo.xml',
        'demo/exam_attendees_demo.xml',
        'demo/grade_configuration_demo.xml',
        'demo/result_template_demo.xml',
        'demo/marksheet_register_demo.xml',
        'demo/marksheet_line_demo.xml',
        'demo/result_line_demo.xml',
    ],
    'images': [
        'static/description/openeducat_exam_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
