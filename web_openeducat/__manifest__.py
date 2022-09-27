# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
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
    'name': 'Web OpenEduCat',
    'category': 'Website',
    "sequence": 3,
    'version': '16.0.1.0',
    'license': 'LGPL-3',
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    'data': [
        'views/assets.xml',
        'views/snippets/slider.xml',
        'views/snippets/about-us.xml',
        'views/snippets/ourcourse.xml',
        'views/snippets/achievement.xml',
        'views/snippets/teacher.xml',
        'views/snippets/event.xml',
        'views/snippets/newsfeed.xml',
        'views/snippets/footer.xml',
        'views/image_library.xml'
    ],
    'qweb': [
        "static/src/xml/base_inherit.xml",
    ],
    'demo': [
        'data/homepage_demo.xml',
        'data/footer_template.xml',
    ],
    'images': [
        'static/description/web_openeducat_banner.jpg',
    ],
    'depends': [
        'website',
    ],
    'application': True,
    'assets': {
        'web.assets_frontend': [
            '/web_openeducat/static/src/scss/homepage.scss',
        ],
    }
}
