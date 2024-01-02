# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
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

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_openeducat_activity = fields.Boolean(string="Activity")
    module_openeducat_facility = fields.Boolean(string="Facility")
    module_openeducat_parent = fields.Boolean(string="Parent")
    module_openeducat_assignment = fields.Boolean(string="Assignment")
    module_openeducat_classroom = fields.Boolean(string="Classroom")
    module_openeducat_fees = fields.Boolean(string="Fees")
    module_openeducat_admission = fields.Boolean(string="Admission")
    module_openeducat_timetable = fields.Boolean(string="Timetable")
    module_openeducat_exam = fields.Boolean(string="Exam")
    module_openeducat_library = fields.Boolean(string="Library")
    module_openeducat_attendance = fields.Boolean(string="Attendance")
    module_openeducat_quiz = fields.Boolean(string="Quiz Enterprise")
    module_openeducat_discipline = fields.Boolean(
        string="Discipline Enterprise")
    module_openeducat_health_enterprise = fields.Boolean(
        string="Health Enterprise")
    module_openeducat_achievement_enterprise = fields.Boolean(
        string="Achievement Enterprise")
    module_openeducat_activity_enterprise = fields.Boolean(
        string="Activity Enterprise")
    module_openeducat_admission_enterprise = fields.Boolean(
        string="Admission Enterprise")
    module_openeducat_alumni_enterprise = fields.Boolean(
        string="Alumni Enterprise")
    module_openeducat_alumni_blog_enterprise = fields.Boolean(
        string="Alumni Blog Enterprise")
    module_openeducat_alumni_event_enterprise = fields.Boolean(
        string="Alumni Event Enterprise")
    module_openeducat_alumni_job_enterprise = fields.Boolean(
        string="Alumni Job Enterprise")
    module_openeducat_job_enterprise = fields.Boolean(
        string="Job Enterprise")
    module_openeducat_assignment_enterprise = fields.Boolean(
        string="Assignment Enterprise")
    module_openeducat_assignment_rubrics = fields.Boolean(
        string="Assignment Rubrics")
    module_openeducat_attendance_enterprise = fields.Boolean(
        string="Attendance Enterprise")
    module_openeducat_student_attendance_enterprise = fields.Boolean(
        string="Student Attendance Kiosk")
    module_openeducat_bigbluebutton = fields.Boolean(
        string="Bigbluebutton Enterprise")
    module_openeducat_campus_enterprise = fields.Boolean(
        string="Campus Enterprise")
    module_openeducat_classroom_enterprise = fields.Boolean(
        string="Classroom Enterprise")
    module_openeducat_exam_enterprise = fields.Boolean(
        string="Exam Enterprise")
    module_openeducat_facility_enterprise = fields.Boolean(
        string="Facility Enterprise")
    module_openeducat_fees_enterprise = fields.Boolean(
        string="Fees Enterprise")
    module_openeducat_fees_plan = fields.Boolean(
        string="Fees Plan")
    module_openeducat_fees_parent_bridge = fields.Boolean(
        string="Fees Parent Bridge")
    module_openeducat_library_barcode = fields.Boolean(
        string="Library Barcode Enterprise")
    module_openeducat_library_enterprise = fields.Boolean(
        string="Library Enterprise")
    module_openeducat_lms = fields.Boolean(
        string="LMS Enterprise")
    module_openeducat_lms_blog = fields.Boolean(
        string="LMS Blog Enterprise")
    module_openeducat_lms_forum = fields.Boolean(
        string="LMS Forum Enterprise")
    module_openeducat_lms_gamification = fields.Boolean(
        string="LMS Gamification Enterprise")
    module_openeducat_lms_sale = fields.Boolean(
        string="LMS Sale Enterprise")
    module_openeducat_lms_survey = fields.Boolean(
        string="LMS Survey Enterprise")
    module_openeducat_meeting_enterprise = fields.Boolean(
        string="Meeting Enterprise")
    module_openeducat_online_admission = fields.Boolean(
        string="Online Admission Enterprise")
    module_openeducat_parent_enterprise = fields.Boolean(
        string="Parent Enterprise")
    module_openeducat_placement_enterprise = fields.Boolean(
        string="Placement Enterprise")
    module_openeducat_placement_job_enterprise = fields.Boolean(
        string="Placement Job Enterprise")
    module_openeducat_scholarship_enterprise = fields.Boolean(
        string="Scholarship Enterprise")
    module_openeducat_timetable_enterprise = fields.Boolean(
        string="Timetable Enterprise")
    module_openeducat_transportation_enterprise = fields.Boolean(
        string="Transportation Enterprise")
    module_openeducat_lesson = fields.Boolean(
        string="Lesson Enterprise")
    module_openeducat_skill_enterprise = fields.Boolean(
        string="Skill Enterprise")
    module_openeducat_lms_website = fields.Boolean(
        string="LMS Website")
    module_openeducat_assignment_grading_enterprise = fields.Boolean(
        string="Assignment Grading Enterprise")
    module_openeducat_assignment_grading_bridge = fields.Boolean(
        string="Assignment Grading Bridge")
    module_openeducat_fees_on_session = fields.Boolean(
        string="Fees On Session")
    module_openeducat_fees_on_duration = fields.Boolean(
        string="Fees On Duration")
    module_openeducat_lms_admission = fields.Boolean(
        string="LMS Admission")
    module_openeducat_backend_theme = fields.Boolean(
        string="Backend Theme")
    module_openeducat_crm_enterprise = fields.Boolean(
        string="CRM Enterprise")
    module_openeducat_dashboard_kpi = fields.Boolean(
        string="Dashboard KPI")
    module_openeducat_digital_library = fields.Boolean(
        string="Digital Library")
    module_openeducat_event_enterprise = fields.Boolean(
        string="Event Enterprise")
    module_openeducat_exam_gpa_enterprise = fields.Boolean(
        string="Exam GPA Enterprise")
    module_openeducat_exam_grading_bridge = fields.Boolean(
        string="Exam Grading Bridge")
    module_openeducat_googlemeet = fields.Boolean(
        string="Google Meet")
    module_openeducat_grading = fields.Boolean(
        string="Grading")
    module_openeducat_jitsi_enterprise = fields.Boolean(
        string="Jitsi Enterprise")
    module_openeducat_quiz_anti_cheating = fields.Boolean(
        string="Quiz Anti Cheating")
    module_openeducat_skypemeet = fields.Boolean(
        string="Skype Meet")
    module_openeducat_student_progress_enterprise = fields.Boolean(
        string="Student Progress Enterprise")
    module_openeducat_subject_material_allocation = fields.Boolean(
        string="Subject Material Allocation")
    module_openeducat_teams = fields.Boolean(
        string="Teams")
    module_openeducat_zoom = fields.Boolean(
        string="Zoom")
    module_openeducat_student_leave_enterprise = fields.Boolean(
        string="Student Leave")
    module_openeducat_notice_board_enterprise = fields.Boolean(
        string="Notice Board Enterprise")
    module_openeducat_student_skill_assessment = fields.Boolean(
        string="Skill Assessment Enterprise")
    module_openeducat_lms_h5p = fields.Boolean(
        string="LMS H5P Enterprise")
    module_openeducat_online_appointment = fields.Boolean(
        string="Online Appointment Enterprise")
    module_openeducat_grievance_enterprise = fields.Boolean(
        string="Grievance")
    module_openeducat_secure = fields.Boolean(
        string="Secure QR")
    module_openeducat_mass_subject_registration = fields.Boolean(
        string="Mass Subject Registration")
    module_openeducat_attendance_report_xlsx = fields.Boolean(
        string="Attendance Xlsx Report")
    module_openeducat_asset_request_enterprise = fields.Boolean(
        string="Asset Request Enterprise")
    module_openeducat_lms_interactive_video = fields.Boolean(
        string="Lms Interactive Video")
    module_openeducat_lms_drag_into_text = fields.Boolean(
        string="Lms Drag Into Text")
    module_openeducat_lms_match_following = fields.Boolean(
        string="Lms Match Following")
    module_openeducat_lms_match_images = fields.Boolean(
        string="Lms Match Images")
    module_openeducat_lms_multiple_choice = fields.Boolean(
        string="Lms Multiple Choice")
    module_openeducat_lms_numeric = fields.Boolean(
        string="Lms Numeric")
    module_openeducat_lms_sort_paragraphs = fields.Boolean(
        string="Lms Sort Paragraphs")
    module_openeducat_quiz_drag_into_text = fields.Boolean(
        string="Quiz Drag Into Text")
    module_openeducat_quiz_match_following = fields.Boolean(
        string="Quiz Match Following")
    module_openeducat_quiz_match_images = fields.Boolean(
        string="Quiz Match Images")
    module_openeducat_quiz_multiple_choice = fields.Boolean(
        string="Quiz Multiple Choice")
    module_openeducat_quiz_numeric = fields.Boolean(
        string="Quiz Numeric")
    module_openeducat_quiz_sort_paragraphs = fields.Boolean(
        string="Quiz Sort Paragraphs")
    module_openeducat_live = fields.Boolean(
        string="Live Meeting")
    module_openeducat_live_assignment = fields.Boolean(
        string="Live Meeting Assignment")
    module_openeducat_live_attendance = fields.Boolean(
        string="Live Meeting Attendance")
    module_openeducat_live_attentiveness = fields.Boolean(
        string="Live Meeting Attentiveness")
    module_openeducat_attendance_face_recognition = fields.Boolean(
        string="Attendance Face Recognition")
    module_openeducat_omr = fields.Boolean(
        string="OMR")
    module_openeducat_auto_database_backup = fields.Boolean(
        string="Database Backup to Local Server")
    module_openeducat_auto_database_backup_dropbox = fields.Boolean(
        string="Database Backup to Dropbox")
    module_openeducat_auto_database_backup_ftp = fields.Boolean(
        string="Database Backup to Remote FTP Server")
    module_openeducat_auto_database_backup_google_drive = fields.Boolean(
        string="Database Backup to Google Drive")
    module_openeducat_auto_database_backup_onedrive = fields.Boolean(
        string="Database Backup to Onedrive")
    module_openeducat_auto_database_backup_sftp = fields.Boolean(
        string="Database Backup to Remote SFTP Server")
    attendance_subject_generic = fields.Selection([('subject', 'Subject Wise'), ('generic', 'Generic')],
                                                  help="Subject-specific attendance will be gathered during a "
                                                       "particular session, whereas general attendance will be "
                                                       "collected by one responsible faculty member for the "
                                                       "entire day.",
                                                  config_parameter="attendance_subject_generic_parameter",
                                                  default='subject')
