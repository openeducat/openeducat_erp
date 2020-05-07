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
    'name': 'OpenEduCat Core',
    'version': '13.0',
    'license': 'LGPL-3',
    'category': 'Education',
    "sequence": 1,
    'summary': 'Manage Students, Faculties and Education Institute',
    'complexity': "easy",
    'author': 'Tech Receptives',
    'website': 'http://www.openeducat.org',
    'depends': ['board', 'hr', 'web', 'website'],
    'data': [
        'security/op_security.xml',
        'security/ir.model.access.csv',
        'report/report_menu.xml',
        'report/report_student_bonafide.xml',
        'report/report_student_idcard.xml',
        'wizard/faculty_create_employee_wizard_view.xml',
        'wizard/faculty_create_user_wizard_view.xml',
        'wizard/students_create_user_wizard_view.xml',
        'views/department_view.xml',
        'views/res_company_view.xml',
        'views/student_view.xml',
        'views/hr_view.xml',
        'views/category_view.xml',
        'views/course_view.xml',
        'views/batch_view.xml',
        'views/subject_view.xml',
        'views/faculty_view.xml',
        'views/website_assets.xml',
        'views/subject_registration_view.xml',
        'views/res_config_setting_view.xml',
        'views/student_portal_view.xml',
        'views/student_course_view.xml',
        'data/ir_cron_data.xml',
        'menu/openeducat_core_menu.xml',
        'menu/faculty_menu.xml',
        'menu/student_menu.xml',
    ],
    'demo': [
        'demo/homepage_template.xml',
        'demo/department_demo.xml',
        'demo/base_demo.xml',
        'demo/res_partner_demo.xml',
        'demo/res_users_demo.xml',
        'demo/subject_demo.xml',
        'demo/course_demo.xml',
        'demo/batch_demo.xml',
        'demo/student_demo.xml',
        'demo/student_course_demo.xml',
        'demo/faculty_demo.xml',
        'demo/res_condig_fav_icon.xml',
    ],
    'css': [
        'static/src/scss/base.scss'
    ],
    'qweb': [
        'static/src/xml/base.xml',
        'static/src/xml/dashboard_ext_openeducat.xml'
    ],
    'js': [],
    'images': [
        'static/description/openeducat_core_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
