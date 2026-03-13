# openeducat_admission – Admissions & Enrolment 🎟️

## Overview

The **Admission** module manages the end-to-end enrolment workflow: from initial application, through document review, to formal admission and student creation.

---

## Key Features

* Online application form capture
* Document checklist and verification
* Multi-stage approval workflow (Applied → Under Review → Admitted / Rejected)
* Automatic `op.student` record creation on admission
* Batch / class assignment at admission time

---

## Core Model: `op.admission`

| Field | Description |
|-------|-------------|
| `name` | Applicant's full name |
| `course_id` | Course applied for |
| `batch_id` | Batch applied for |
| `state` | Draft → Submitted → Under Review → Admitted / Rejected |
| `student_id` | Linked student (populated on admission) |
| `date_of_birth` | Applicant DOB |
| `gender` | Male / Female |
| `parent_id` | Parent / guardian link |

---

## Workflow

```
Draft ──▶ Submitted ──▶ Under Review ──▶ Admitted ──▶ [Student created]
                                      └──▶ Rejected
```

---

## License

LGPL-3.0 – see repository [LICENSE](../LICENSE).
