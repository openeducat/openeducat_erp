# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
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
