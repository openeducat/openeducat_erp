###############################################################################
#
#    openEMIS
#    Copyright (C) 2009-TODAY openEMIS(<https://www.openemis.org>).
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
    'name': 'openEMIS Blog',
    'version': '18.0.1.0',
    'license': 'LGPL-3',
    'category': 'Education',
    'sequence': 7,
    'summary': (
        'Educational blog where mentors, teachers and parents share '
        'articles accessible to all students'
    ),
    'description': """
Educational Blog
=================
This module provides a dedicated educational blog platform where:

* **Mentors**, **teachers**, **parents** and **professionals** can
  write and publish blog posts and educational articles.
* Posts are tagged with subjects, grade levels and topics for easy
  discovery.
* All students have read access to published articles.
* Posts can include attachments (PDFs, videos, images).
* A comment system allows students to engage with articles.
    """,
    'author': 'openEMIS',
    'website': 'https://www.openemis.org',
    'depends': [
        'mail',
        'openeducat_core',
    ],
    'data': [
        'security/op_security.xml',
        'security/ir.model.access.csv',
        'views/blog_category_view.xml',
        'views/blog_post_view.xml',
        'views/blog_comment_view.xml',
        'menus/op_menu.xml',
    ],
    'demo': [
        'demo/blog_category_demo.xml',
        'demo/blog_post_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
