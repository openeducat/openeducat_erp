# openeducat_exam – Examination Management 📊

## Overview

The **Exam** module manages the full examination cycle: scheduling exams, recording results, computing grade letters and generating mark sheets.  Results recorded here feed directly into the **DigiGuide** module's national-exam prediction engine.

---

## Key Features

* Exam scheduling per course, batch and subject
* Mark sheet recording (per student, per subject)
* Configurable grade letter bands (A–E or custom)
* Automatic result computation and pass/fail determination
* Mark sheet print reports
* Distinction between internal exams and official national exams

---

## Core Models

### `op.exam`

| Field | Description |
|-------|-------------|
| `name` | Exam name (e.g. "Grade 6 End-of-Year 2024") |
| `course_id` | Course / grade |
| `exam_date` | Date of examination |
| `total_marks` | Maximum marks |
| `state` | Draft → Scheduled → In Progress → Completed |

### `op.exam.result`

| Field | Description |
|-------|-------------|
| `exam_id` | Linked exam |
| `student_id` | Student |
| `marks_obtained` | Score |
| `grade` | Grade letter computed from marks |
| `result` | Pass / Fail |

---

## Grade Configuration

Grade bands are configurable per exam or globally.  The default CBC-aligned bands are:

| Marks | Grade Letter |
|-------|-------------|
| 80 – 100 | A |
| 70 – 79 | B |
| 60 – 69 | C |
| 50 – 59 | D |
| 0 – 49 | E |

---

## License

LGPL-3.0 – see repository [LICENSE](../LICENSE).
