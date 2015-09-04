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
    'name': 'OpenEduCat ERP',
    'version': '1.2.0',
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
    'depends': ['account_accountant', 'document',
                'hr', 'web', 'website'],
    'data': [
        'security/op_security.xml',
        'op_activity/op_activity_view.xml',
        'op_parent/op_parent_view.xml',
        'op_student/op_student_view.xml',
        'op_standard/op_standard_view.xml',
        'op_health/op_health_view.xml',
        'op_route/op_route_view.xml',
        'op_faculty/op_faculty_view.xml',
        'op_admission/op_admission_view.xml',
        'op_admission/op_admission_sequence.xml',
        'op_hostel_room/op_hostel_room_view.xml',
        'op_attendance_register/op_attendance_register_view.xml',
        'op_category/op_category_view.xml',
        'op_attendance_sheet/op_attendance_sheet_view.xml',
        'op_exam/op_exam_view.xml',
        'op_publisher/op_publisher_view.xml',
        'op_religion/op_religion_view.xml',
        'op_attendance_line/op_attendance_line_view.xml',
        'op_transportation/op_transportation_view.xml',
        'op_book_movement/op_book_movement_view.xml',
        'op_book_queue/op_book_queue_view.xml',
        'op_book_queue/op_book_queue_sequence.xml',
        'op_division/op_division_view.xml',
        'op_placement_offer/op_placement_offer_view.xml',
        'op_marksheet_register/op_marksheet_register_view.xml',
        'op_classroom/op_classroom_view.xml',
        'op_vehicle/op_vehicle_view.xml',
        'op_hostel/op_hostel_view.xml',
        'op_exam_attendees/op_exam_attendees_view.xml',
        'wizard/exam_seating_arrangement_view.xml',
        'wizard/book_request_queue_view.xml',
        'wizard/issue_book_view.xml',
        'wizard/return_book_view.xml',
        'wizard/student_hall_tickets_wizard_view.xml',
        'wizard/admission_analysis_wizard_view.xml',
        'wizard/wizard_op_student_view.xml',
        'op_book/op_book_view.xml',
        'op_batch/op_batch_view.xml',
        'op_marksheet_line/op_marksheet_line_view.xml',
        'op_course/op_course_view.xml',
        'op_subject/op_subject_view.xml',
        'op_tag/op_tag_view.xml',
        'op_result_line/op_result_line_view.xml',
        'op_author/op_author_view.xml',
        'op_exam_type/op_exam_type_view.xml',
        'op_facility/op_facility_view.xml',
        "op_faculty/hr_view.xml",
        'op_scholarship/op_scholarship_view.xml',
        'op_scholarship_type/op_scholarship_type_view.xml',
        'op_roll_number/op_roll_number_view.xml',
        'op_library/op_library_view.xml',
        'op_timetable/op_timetable_view.xml',
        'op_assignment/op_assignment_view.xml',
        'op_assignment_sub_line/op_assignment_sub_line_view.xml',
        'op_assignment_sub_history/op_assignment_sub_history_view.xml',
        'op_achievement/op_achievement_view.xml',
        'op_achievement_type/op_achievement_type_view.xml',
        'op_exam_res_allocation/op_exam_res_allocation_view.xml',
        'op_exam_room/op_exam_room_view.xml',
        'op_allocat_division/op_allocat_division_view.xml',
        'wizard/generate_roll_number_view.xml',
        'wizard/generate_time_table_view.xml',
        'wizard/time_table_report.xml',
        'wizard/op_all_student_wizard_view.xml',
        'wizard/student_attendance_report_view.xml',
        'wizard/student_migrate_view.xml',
        'security/ir.model.access.csv',
        'op_book_movement/wizard/returndate_view.xml',
        'op_book_movement/wizard/reserve_book_view.xml',
        'op_result_template/op_result_template_view.xml',
        'menu/openeducat_erp_menu.xml',
        'report/report_menu.xml',
        'op_book_purchase/op_book_purchase_view.xml',
        'dashboard/librarian_dashboard_view.xml',
        'dashboard/faculty_dashboard_view.xml',
        'dashboard/student_dashboard_view.xml',
        'menu/student_menu.xml',
        'menu/faculty_menu.xml',
        'menu/library_menu.xml',
        'menu/parent_menu.xml',
        'op_exam/op_exam_workflow.xml',
        'op_admission/op_admission_workflow_view.xml',
        'res_company/res_company.xml',
        'views/report_admission_analysis.xml',
        'views/report_bonafide_certificate.xml',
        'views/report_book_barcode.xml',
        'views/student_marksheet.xml',
        'views/transportation.xml',
        'views/student_idcard.xml',
        'views/library_idcard.xml',
        'views/report_ticket.xml',
        'views/student_label.xml',
        'views/report_time_table_teacher_generate.xml',
        'views/generate_timetable_student.xml',
        'views/openeducat_template.xml',
        'views/homepage_template.xml',

    ],
    'demo': [
        'demo/res.users.csv',
        'demo/res.groups.csv',
        'demo/op.category.csv',
        'demo/op.course.csv',
        'demo/op.subject.csv',
        'demo/op.batch.csv',
        'demo/op.standard.csv',
        'demo/op.religion.csv',
        'demo/op.tag.csv',
        'demo/op.book.csv',
        'demo/op.author.csv',
        'demo/op.division.csv',
        'demo/op.student.csv',
        'demo/op.faculty.csv',
        'demo/op.exam.type.csv',
        'demo/op.period.csv',
        'demo/op_comapny_data.xml',
        'demo/op.book.queue.csv',
        'demo/op.assignment.csv',
        'demo/op_timetable_data.xml',
        'demo/op.assignment.sub.line.csv',
    ],
    'css': ['static/src/css/base.css'],
    'qweb': [
        'static/src/xml/base.xml'],
    'js': ['static/src/js/chrome.js'],
    'test': [
        'test/configuration.yml',
        'test/new_admission.yml',
        'test/new_faculty.yml'
    ],
    'images': [
        'images/Admission_Process.png',
        'images/Course_list.png',
        'images/Faculty_management.png',
        'images/Student_Information.png',
        'images/TimeTable.png'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
