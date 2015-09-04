# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

{
    'name': 'Indian OpenEduCat',
    'version': '2.0.0',
    'category': 'Openerp Education',
    "sequence": 3,
    'summary': 'Indian Localization of OpenEduCat',
    'complexity': "easy",
    'description': """
        This module adds Indian flavor to OpenEduCat_Core.

    """,
    'author': 'Tech Receptives',
    'website': 'http://www.openeducat.org',
    'depends': ['openeducat_core'],
    'data': [
        'views/student_view.xml',
        'views/faculty_view.xml',
        'views/category_view.xml',
        'views/religion_view.xml',
        'security/ir.model.access.csv'
    ],
    'demo': [
        'demo/op.category.csv',
        'demo/op.religion.csv',
        'demo/op.student.csv',
        'demo/op.faculty.csv'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
