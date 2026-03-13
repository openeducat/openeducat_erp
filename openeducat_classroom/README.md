# openeducat_classroom – Classroom Management 🏫

## Overview

The **Classroom** module manages the physical and virtual learning spaces at an institution.  Classrooms are referenced by the timetable module when scheduling sessions.

---

## Key Features

* Maintain a register of all classrooms with capacity and type
* Mark rooms as available or under maintenance
* Integration with timetable for conflict detection
* Facility booking for special events

---

## Core Model: `op.classroom`

| Field | Description |
|-------|-------------|
| `name` | Room name / number (e.g. "R001", "Science Lab 2") |
| `code` | Short code |
| `capacity` | Maximum student capacity |
| `type` | Classroom / Laboratory / Hall / Library / Virtual |
| `state` | Available / Occupied / Under Maintenance |

---

## License

LGPL-3.0 – see repository [LICENSE](../LICENSE).
