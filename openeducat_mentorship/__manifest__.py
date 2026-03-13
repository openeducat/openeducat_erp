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
    'name': 'openEMIS Mentorship',
    'version': '18.0.1.0',
    'license': 'LGPL-3',
    'category': 'Education',
    'sequence': 6,
    'summary': (
        'Connect students with mentors – professionals, teachers and '
        'parents – via direct messages and group discussion forums'
    ),
    'description': """
Mentorship Platform
====================
This module provides a dedicated mentorship space where:

* **Mentors** (professionals, dedicated parents and teachers) register
  and receive approval before they can interact with students.
* Students can send **Direct Messages (DMs)** to approved mentors on
  specific subjects, topics or questions.
* Students and mentors can join **Group Forums** where questions are
  posted, categorised and routed to the most relevant mentors.
* An AI-assisted **subject tagging** layer categorises incoming
  questions and suggests the most appropriate mentor group.
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
        'views/mentor_view.xml',
        'views/mentorship_group_view.xml',
        'views/mentorship_message_view.xml',
        'menus/op_menu.xml',
    ],
    'demo': [
        'demo/mentor_demo.xml',
        'demo/mentorship_group_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
