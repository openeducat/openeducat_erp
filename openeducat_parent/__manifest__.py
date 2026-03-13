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
    'name': 'openEMIS Parent',
    'version': '18.0.1.0',
    'license': 'LGPL-3',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Manage Parent',
    'complexity': "easy",
    'author': 'openEMIS',
    'website': 'https://www.openemis.org',
    'depends': ['openeducat_core'],
    'data': [
        'security/op_security.xml',
        'security/ir.model.access.csv',
        'data/parent_user_data.xml',
        'views/parent_view.xml',
        'views/parent_relationship_view.xml',
        'menus/op_menu.xml',
        'report/report_student_bonafide_inherit.xml',
    ],
    'demo': [
        'demo/res_partner_demo.xml',
        'demo/openemis_parent_bulk_partners.xml',
        'demo/res_users_demo.xml',
        'demo/openemis_parent_bulk_users.xml',
        'demo/parent_relationship_demo.xml',
        'demo/parent_demo.xml',
        'demo/openemis_parent_bulk.xml',
    ],
    'images': [
        'static/description/openeducat-parent_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
