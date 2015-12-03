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
    'version': '2.4.0',
    'category': 'Openerp Education',
    "sequence": 3,
    'summary': 'Manage Library',
    'complexity': "easy",
    'description': """
        This module provide feature of Library Management.

    """,
    'author': 'Tech Receptives',
    'website': 'http://www.openeducat.org',
    'depends': ['openeducat_core'],
    'data': [
        'security/library_security.xml',
        'security/ir.model.access.csv',
        'report/report_book_barcode.xml',
        'report/report_student_library_card.xml',
        'report/report_menu.xml',
        'wizards/issue_book_view.xml',
        'wizards/return_book_view.xml',
        'wizards/returndate_view.xml',
        'wizards/reserve_book_view.xml',
        'views/book_view.xml',
        'views/book_unit_view.xml',
        'views/book_movement_view.xml',
        'views/book_purchase_view.xml',
        'views/book_queue_view.xml',
        'views/library_view.xml',
        'views/author_view.xml',
        'views/publisher_view.xml',
        'views/tag_view.xml',
        'views/student_view.xml',
        'views/faculty_view.xml',
        'book_queue_sequence.xml',
        'dashboard/librarian_dashboard_view.xml',
        'menus/library_menu.xml',
    ],
    'demo': [
        'demo/res.users.csv',
        'demo/res.groups.csv',
        'demo/op.tag.csv',
        'demo/op.publisher.csv',
        'demo/op.author.csv',
        'demo/op.book.csv',
        'demo/op.book.unit.csv',
        'demo/op.book.queue.csv',
    ],
    'images': [
        'static/description/openeducat_library_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
