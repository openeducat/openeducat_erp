# openeducat_timetable – Timetable Management 📅

## Overview

The **Timetable** module allows academic administrators to plan and publish class schedules for each batch, mapping subjects, teachers and classrooms to time slots.

---

## Key Features

* Weekly timetable grid per batch
* Teacher and classroom conflict detection
* Period / slot configuration per academic term
* Timetable publication to students and teachers
* Integration with the attendance module (sessions derived from timetable)

---

## Core Models

### `op.timetable`

Represents one class session slot in the timetable.

| Field | Description |
|-------|-------------|
| `batch_id` | Batch / class |
| `subject_id` | Subject being taught |
| `teacher_id` | Assigned teacher |
| `classroom_id` | Assigned room |
| `day_of_week` | Monday – Friday (or Saturday) |
| `start_time` | Period start time |
| `end_time` | Period end time |

---

## License

LGPL-3.0 – see repository [LICENSE](../LICENSE).
