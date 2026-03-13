# openEMIS – System Screenshots

These screenshots document the major modules of the **openEMIS** system – an Open Source Educational Management Information System built on the Odoo ERP framework. The system was brought up locally using Docker with PostgreSQL and populated with demo data.

---

## System Overview

| Screenshot | Module | Description |
|---|---|---|
| [01_main_menu.png](01_main_menu.png) | System Home | Main application home screen showing all installed apps |
| [01_main_navigation_menu.png](01_main_navigation_menu.png) | Navigation | Top navigation bar showing all available modules |
| [24_all_modules_menu.png](24_all_modules_menu.png) | Full Menu | Complete list of all installed modules |

---

## Student Information System (SIS)

| Screenshot | Module | Description |
|---|---|---|
| [02_students.png](02_students.png) | Students (Kanban) | Student kanban view - visual card layout with student profiles |
| [09_sis_students.png](09_sis_students.png) | SIS Students | Student list in SIS module |
| [10_faculties.png](10_faculties.png) | Faculties | Faculty/teacher profiles in kanban view |
| [22_students_list_view.png](22_students_list_view.png) | Students (List) | Students in list view with all fields |
| [21_new_student_form.png](21_new_student_form.png) | New Student Form | Student registration form with personal information |
| [23_sis_general_menu.png](23_sis_general_menu.png) | SIS Navigation | SIS module navigation menu with General section |

---

## Admissions

| Screenshot | Module | Description |
|---|---|---|
| [11_admissions.png](11_admissions.png) | Admission Registers | Admission register management |
| [12_admissions_applications.png](12_admissions_applications.png) | Applications | Student application management and tracking |

---

## Academic Management

| Screenshot | Module | Description |
|---|---|---|
| [13_timetable.png](13_timetable.png) | Time Table | Weekly class schedule in calendar view |
| [14_class_attendances.png](14_class_attendances.png) | Class Attendances | Attendance register management |
| [15_assignments.png](15_assignments.png) | Assignments | Assignment tracking with course, batch, faculty fields |
| [16_exams.png](16_exams.png) | Exams | Exam session management |

---

## Library

| Screenshot | Module | Description |
|---|---|---|
| [17_library.png](17_library.png) | Library Media | Library media/book catalogue management |

---

## Finance & Administration

| Screenshot | Module | Description |
|---|---|---|
| [18_invoicing.png](18_invoicing.png) | Invoicing | Customer invoices with payment status (Paid/Not Paid/Draft) |
| [19_human_resources.png](19_human_resources.png) | Human Resources | Employee management in kanban view |
| [20_dashboards.png](20_dashboards.png) | Dashboards | Finance dashboard with key performance indicators |

---

## System Setup

**Stack:**
- Odoo 18.0 (Community Edition)
- PostgreSQL 15
- openEMIS modules: `openeducat_core`, `openeducat_admission`, `openeducat_exam`,
  `openeducat_attendance`, `openeducat_library`, `openeducat_timetable`,
  `openeducat_assignment`, `openeducat_parent`, `openeducat_activity`,
  `openeducat_facility`, `openeducat_fees`

**Quick Start (Docker):**
```bash
# From the repository root
docker compose up -d
# Wait ~60 seconds for Odoo to initialize
# Visit http://localhost:8069
# Login: admin / admin
```

**Populating 100+ demo records per entity:**
```bash
# (Re-)generate bulk demo XML files
python scripts/generate_demo_data.py
# Then re-install the modules with demo data enabled in Odoo
```
