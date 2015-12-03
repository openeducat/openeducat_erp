# -*- coding: utf-8 -*-
##############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech Receptives(<http://www.techreceptives.com>).
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
##############################################################################

{
    'name': 'OpenEduCat ERP',
    'version': '2.4.0',
    'category': 'Openerp Education',
    "sequence": 3,
    'summary': 'Manage Students, Faculties and Education Institute',
    'complexity': "easy",
    'description': """
        This module provide overall education management system overOpenERP
        Features includes managing
            * Student
            * Faculty
            * Admission
            * Course
            * Batch
            * Standard
            * Books
            * Library
            * Lectures
            * Exams
            * Marksheet
            * Result
            * Transportation
            * Hostel

    """,
    'author': 'Tech Receptives',
    'website': 'http://www.openeducat.org',
    'depends': ['openeducat_achievement', 'openeducat_activity',
                'openeducat_alumni', 'openeducat_assignment',
                'openeducat_attendance', 'openeducat_exam',
                'openeducat_health', 'openeducat_hostel',
                'openeducat_admission', 'openeducat_library',
                'openeducat_parent', 'openeducat_placement',
                'openeducat_scholarship', 'openeducat_timetable',
                'openeducat_transportation'],
    'data': [
    ],
    'demo': [
    ],
    'images': [
        'static/description/openeducat_erp_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
