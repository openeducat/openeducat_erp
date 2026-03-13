# openeducat_attendance – Attendance Tracking ⏰

## Overview

The **Attendance** module tracks daily or session-based attendance for students and faculty.

---

## Key Features

* Session-level attendance (per subject / period)
* Bulk mark-attendance wizard for teachers
* Attendance summary reports (by student, class or period)
* Absence notifications to parents
* Integration with timetable module for session lookup

---

## Core Model: `op.attendance.sheet`

| Field | Description |
|-------|-------------|
| `course_id` | Course |
| `batch_id` | Batch / class |
| `subject_id` | Subject |
| `attendance_date` | Date of session |
| `attendance_ids` | One2many of individual student records |

### `op.attendance.sheet.line`

| Field | Description |
|-------|-------------|
| `student_id` | Student |
| `presence` | Present / Absent / Late / Excused |

---

## License

LGPL-3.0 – see repository [LICENSE](../LICENSE).
