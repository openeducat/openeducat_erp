# openeducat_parent – Parent Portal 👨‍👩‍👧

## Overview

The **Parent** module links parents and guardians to their children's student records, providing a dedicated portal view where parents can monitor attendance, exam results, fee balances and assignments.

---

## Key Features

* Parent–student linking (one parent can have multiple children)
* Parent portal login (Odoo website portal access)
* Read access to attendance, exam marks and fee balance
* In-app notifications for absence, low marks or unpaid fees
* Parent–teacher communication through the Odoo chatter

---

## Core Model: `op.parent`

| Field | Description |
|-------|-------------|
| `partner_id` | Linked `res.partner` |
| `student_ids` | Children (Many2many → `op.student`) |
| `relation` | Father / Mother / Guardian |
| `occupation` | Parent's occupation |

---

## License

LGPL-3.0 – see repository [LICENSE](../LICENSE).
