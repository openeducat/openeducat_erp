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
    'name': 'openEMIS DigiGuide – Digital Career Guidance',
    'version': '18.0.1.0',
    'license': 'LGPL-3',
    'category': 'Education',
    'sequence': 5,
    'summary': (
        'CBC academic performance tracking, national exam prediction '
        'and KUCCPS career guidance integration'
    ),
    'description': """
DigiGuide – Digital Career Guidance
====================================
This module reads incremental CBC academic performance data (weekly
assignments, mid-term, termly and end-of-year exams) for students from
Grade 1 through Grade 12 and college, then:

* Predicts likely performance in national exams (Grade 3, Grade 6,
  Grade 9 – Junior Secondary, Grade 12 – Senior Secondary).
* Integrates with the KUCCPS (Kenya Universities and Colleges Central
  Placement Service) API to fetch career/programme requirements.
* Matches each student's predicted grades and subject combinations
  against KUCCPS career requirements to surface career suitability.
    """,
    'author': 'openEMIS',
    'website': 'https://www.openemis.org',
    'depends': [
        'openeducat_exam',
        'openeducat_assignment',
    ],
    'data': [
        'security/op_security.xml',
        'security/ir.model.access.csv',
        'data/digiguide_data.xml',
        'views/academic_performance_view.xml',
        'views/national_exam_prediction_view.xml',
        'views/kuccps_career_view.xml',
        'views/career_match_view.xml',
        'menus/op_menu.xml',
    ],
    'demo': [
        'demo/kuccps_career_demo.xml',
        'demo/academic_performance_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
