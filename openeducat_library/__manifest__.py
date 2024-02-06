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
    'name': 'OpenEduCat Library',
    'version': '17.0.1.0',
    'license': 'LGPL-3',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Manage Library',
    'complexity': "easy",
    'author': 'OpenEduCat Inc',
    'website': 'https://www.openeducat.org',
    'depends': [
        'account',
        'base_automation',
        'openeducat_activity',
        'openeducat_parent',
    ],
    'data': [
        'security/op_security.xml',
        'security/ir.model.access.csv',
        'data/custom_paperformat.xml',
        'data/media_queue_sequence.xml',
        'data/action_rule_data.xml',
        'data/product_demo.xml',
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
        'menus/op_menu.xml',
    ],
    'demo': [
        'demo/media_type_demo.xml',
        'demo/res_users_demo.xml',
        'demo/tag_demo.xml',
        'demo/publisher_demo.xml',
        'demo/author_demo.xml',
        'demo/media_demo.xml',
        'demo/media_unit_demo.xml',
        'demo/media_queue_demo.xml',
        'demo/library_card_type_demo.xml',
        'demo/library_card_demo.xml',
        'demo/media_movement_demo.xml',
        'demo/media_purchase_demo.xml'
    ],
    'images': [
        'static/description/openeducat_library_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
