# openeducat_fees – Fee & Finance Management 💰

## Overview

The **Fees** module manages the complete fee cycle for an institution: defining fee structures, invoicing students, tracking payments and generating financial reports.

---

## Key Features

* Flexible fee structure configuration (per course, batch or term)
* Automatic invoice generation at term start
* Multiple payment modes (cash, bank transfer, M-Pesa, etc.)
* Partial payment and instalment tracking
* Outstanding balance reports and reminders
* Integration with Odoo accounting (`account.move`)

---

## Core Models

### `op.fees.structure`

Defines what fees are charged for a given course/batch/term.

| Field | Description |
|-------|-------------|
| `name` | Structure name |
| `course_id` | Course |
| `academic_term_id` | Academic term |
| `line_ids` | Individual fee line items |

### `op.fees.structure.line`

| Field | Description |
|-------|-------------|
| `name` | Fee component (e.g. Tuition, Activity Fee) |
| `amount` | Amount in institution currency |

### `op.student.fees.detail`

Per-student invoice/payment record.

| Field | Description |
|-------|-------------|
| `student_id` | Student |
| `fees_structure_id` | Applied fee structure |
| `amount` | Total amount due |
| `amount_paid` | Amount received |
| `state` | Unpaid → Partial → Paid |

---

## License

LGPL-3.0 – see repository [LICENSE](../LICENSE).
