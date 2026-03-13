# openeducat_assignment – Assignment Management 📝

## Overview

The **Assignment** module enables teachers to create, distribute and grade assignments for students.  Graded results feed into the DigiGuide module's academic performance data store.

---

## Key Features

* Create assignments per course, batch and subject
* Set due dates and maximum marks
* Students submit work (file attachments supported)
* Teachers grade submissions and leave feedback
* Grade sheet reporting

---

## Core Models

### `op.assignment`

| Field | Description |
|-------|-------------|
| `name` | Assignment title |
| `course_id` | Target course |
| `subject_id` | Subject |
| `deadline` | Submission deadline |
| `marks` | Maximum marks |
| `state` | Draft → Open → Closed |

### `op.assignment.submission`

| Field | Description |
|-------|-------------|
| `assignment_id` | Parent assignment |
| `student_id` | Submitting student |
| `submission_date` | When submitted |
| `marks_obtained` | Score awarded by teacher |
| `feedback` | Teacher comments |

---

## License

LGPL-3.0 – see repository [LICENSE](../LICENSE).
