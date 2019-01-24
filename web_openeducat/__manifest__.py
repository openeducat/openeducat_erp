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
    'name': 'Web OpenEduCat',
    'description': 'Beautifies Website',
    'category': 'Website',
    "sequence": 3,
    'version': '12.0',
    'license': 'LGPL-3',
    'author': 'Tech Receptives',
    'website': 'http://www.openeducat.org',
    'data': [
        'views/assets.xml',
        'views/navbar_template.xml',
        'views/snippets/snippet_banner.xml',
        'views/snippets/snippet_services.xml',
        'views/snippets/snippet_three_image.xml',
        'views/snippets/snippet_cta.xml',
        'views/snippets/snippet_team.xml',
        'views/snippets/snippet_blog.xml',
    ],
    'demo': [
        # 'demo/homepage.xml',
        'demo/footer_template.xml',
        'demo/feature_template.xml',
    ],
    'images': [
        'static/description/web_openeducat_banner.jpg',
    ],
    'depends': [
        'website',
    ],
}
