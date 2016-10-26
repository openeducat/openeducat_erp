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
    'name': 'OpenEduCat Library',
    'version': '9.0.2.4.0',
    'license': 'LGPL-3',
    'category': 'Openerp Education',
    "sequence": 3,
    'summary': 'Manage Library',
    'complexity': "easy",
    'description': """
        This module provide feature of Library Management.

    """,
    'author': 'Tech Receptives',
    'website': 'http://www.openeducat.org',
    'depends': ['openeducat_core', 'account_accountant', 'openeducat_activity'],
    'data': [
        'security/library_security.xml',
        'security/ir.model.access.csv',
        'report/report_media_barcode.xml',
        'report/report_library_card_barcode.xml',
        'report/report_student_library_card.xml',
        'report/report_menu.xml',
        'wizards/issue_media_view.xml',
        'wizards/return_media_view.xml',
        'wizards/reserve_media_view.xml',
        'views/media_view.xml',
        'views/media_unit_view.xml',
        'views/media_movement_view.xml',
        'views/media_purchase_view.xml',
        'views/media_queue_view.xml',
        'views/library_view.xml',
        'views/author_view.xml',
        'views/publisher_view.xml',
        'views/tag_view.xml',
        'views/media_type_view.xml',
        'views/student_view.xml',
        'views/faculty_view.xml',
        'dashboard/library_student_dashboard.xml',
        'media_queue_sequence.xml',
        'menus/library_menu.xml',
    ],
    'demo': [
        'demo/product_demo.xml',
        'demo/media_type_demo.xml',
        'demo/res_users_demo.xml',
        'demo/res_groups_demo.xml',
        'demo/tag_demo.xml',
        'demo/publisher_demo.xml',
        'demo/author_demo.xml',
        'demo/media_demo.xml',
        'demo/media_unit_demo.xml',
        'demo/media_queue_demo.xml',
        'demo/library_card_type_demo.xml',
        'demo/library_card_demo.xml',
        'demo/media_movement_demo.xml',
    ],
    'images': [
        'static/description/openeducat_library_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
