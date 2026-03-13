# openeducat_core – Foundation Module 🏗️

## Overview

`openeducat_core` is the **foundation** of openEMIS.  Every other module in the suite depends on it.  It defines the core data models that represent an educational institution: students, teachers, courses, subjects, academic years, terms and faculties.

---

## Module Structure

```
openeducat_core/
├── __init__.py
├── __manifest__.py
├── demo/                        # Sample data (students, courses, subjects …)
├── models/
│   ├── academic_term.py         # op.academic.term
│   ├── academic_year.py         # op.academic.year
│   ├── course.py                # op.course
│   ├── faculty.py               # op.faculty
│   ├── op_subject.py            # op.subject
│   ├── student.py               # op.student
│   └── teacher.py               # op.teacher (faculty member)
├── security/
│   ├── ir.model.access.csv
│   └── op_security.xml
├── views/
│   ├── course_view.xml
│   ├── faculty_view.xml
│   ├── student_view.xml
│   └── ...
└── wizard/
    └── ...
```

---

## Core Models

### `op.student`
Represents a learner enrolled at the institution.

| Field | Description |
|-------|-------------|
| `gr_no` | Unique admission / grade roll number |
| `first_name`, `last_name` | Name fields |
| `gender` | Male / Female |
| `partner_id` | Linked `res.partner` for contact details |
| `course_id` | Current course |
| `batch_id` | Current batch/class |
| `nationality` | Country of origin |
| `blood_group` | Medical info |

### `op.teacher`
A faculty member who teaches one or more subjects.  Linked to `hr.employee`.

### `op.course`
A programme of study (e.g. "Grade 7 – Junior Secondary").

### `op.subject`
A single subject within a course (e.g. Mathematics, Biology).

### `op.faculty`
An academic department or school (e.g. Faculty of Science).

### `op.academic.year` / `op.academic.term`
Calendar structures that define when terms start and end.

---

## Security Groups

| Group | Permissions |
|-------|-------------|
| Student | View own data only |
| Teacher | View students, manage own records |
| Academic Manager | Full access to all academic data |

---

## License

LGPL-3.0 – see repository [LICENSE](../LICENSE).
