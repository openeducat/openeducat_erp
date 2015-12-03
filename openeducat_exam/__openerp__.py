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
    'name': 'OpenEduCat Exam',
    'version': '2.4.0',
    'category': 'Openerp Education',
    "sequence": 3,
    'summary': 'Manage Exam',
    'complexity': "easy",
    'description': """
        This module provide exam management system over OpenERP
    """,
    'author': 'Tech Receptives',
    'website': 'http://www.openeducat.org',
    'depends': ['openeducat_classroom'],
    'data': [
        'views/exam_attendees_view.xml',
        'views/exam_res_allocation_view.xml',
        'views/exam_room_view.xml',
        'views/exam_session_view.xml',
        'views/exam_type_view.xml',
        'views/exam_view.xml',
        'views/marksheet_line_view.xml',
        'views/marksheet_register_view.xml',
        'views/min_clearance_criteria_view.xml',
        'views/pass_status_view.xml',
        'views/result_exam_line_view.xml',
        'views/result_line_view.xml',
        'views/result_template_line_view.xml',
        'views/result_template_view.xml',
        'report/report_ticket.xml',
        'report/student_marksheet.xml',
        'report/report_exam_student_label.xml',
        'report/report_menu.xml',
        'wizard/student_hall_tickets_wizard_view.xml',
        'security/ir.model.access.csv',
        'exam_menu.xml',
    ],
    'demo': [
        'demo/op.classroom.csv',
        'demo/op.exam.room.csv',
        'demo/op.exam.type.csv',
        'demo/op.exam.session.csv',
        'demo/op.exam.csv',
        'demo/op.exam.attendees.csv'
    ],
    'images': [
        'static/description/openeducat_exam_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
