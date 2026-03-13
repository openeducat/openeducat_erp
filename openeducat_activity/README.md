# openeducat_activity – Activity Management 🏃

## Overview

The **Activity** module manages extra-curricular and co-curricular activities at the institution – sports, clubs, arts, community service and more.

---

## Key Features

* Define activities with categories (sport, arts, community, etc.)
* Enrol students into activities
* Track activity sessions and participation records
* Award certificates or merit points for participation
* Reporting on student activity participation history

---

## Core Model: `op.activity`

| Field | Description |
|-------|-------------|
| `name` | Activity name (e.g. "Football", "Drama Club") |
| `category` | Category (Sport / Arts / Community / Academic) |
| `teacher_id` | Supervising teacher |
| `student_ids` | Enrolled students |
| `max_participants` | Maximum enrolment |

---

## License

LGPL-3.0 – see repository [LICENSE](../LICENSE).
