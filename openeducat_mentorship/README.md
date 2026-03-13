# openeducat_mentorship – Mentorship Platform 🤝

## Overview

The **Mentorship** module connects students with approved mentors – professionals from industry, dedicated parents and experienced teachers – through a structured, safe platform that offers:

* **Direct Messages (DMs)** – A student can send a private message directly to an approved mentor on a specific subject, topic or question.
* **Group Discussion Forums** – Students join themed groups (e.g. "STEM Study Circle") and post questions.  Approved mentors respond, and an AI-assisted tagging layer routes questions to the most relevant mentor within the group.
* **Mentor Approval Workflow** – Mentors register and must be approved by a platform manager before they can interact with students, ensuring a safe environment.

---

## Module Structure

```
openeducat_mentorship/
├── __init__.py
├── __manifest__.py
├── demo/
│   ├── mentor_demo.xml             # 2 sample mentors (professional & teacher)
│   └── mentorship_group_demo.xml   # 2 sample groups
├── menus/
│   └── op_menu.xml
├── models/
│   ├── __init__.py
│   ├── mentor.py                   # op.mentor
│   ├── mentorship_group.py         # op.mentorship.group
│   └── mentorship_message.py      # op.mentorship.message
├── security/
│   ├── ir.model.access.csv
│   └── op_security.xml
├── tests/
│   ├── __init__.py
│   └── test_mentorship.py
└── views/
    ├── mentor_view.xml
    ├── mentorship_group_view.xml
    └── mentorship_message_view.xml
```

---

## Models

### `op.mentor`

Represents an adult who has registered to mentor students.

| Field | Type | Description |
|-------|------|-------------|
| `partner_id` | Many2one → `res.partner` | Linked contact record |
| `name` | Char (related) | Full name |
| `email` | Char (related) | Email address |
| `mentor_type` | Selection | Professional / Teacher / Parent |
| `state` | Selection | Pending → Approved / Suspended / Rejected |
| `profession` | Char | Job title or role |
| `bio` | Text | Profile / biography |
| `expertise_subject_ids` | Many2many → `op.subject` | Subjects the mentor can help with |
| `approved_by` | Many2one → `res.users` | Manager who approved the mentor |
| `approval_date` | Datetime | When the approval was granted |
| `group_ids` | Many2many → `op.mentorship.group` | Groups the mentor belongs to |

**Lifecycle actions:** `action_approve` → `action_suspend` / `action_reject` → `action_reset_pending`

### `op.mentorship.group`

A themed discussion space.

| Field | Type | Description |
|-------|------|-------------|
| `name` | Char | Group name (e.g. "STEM Study Circle") |
| `description` | Text | What the group is about |
| `subject_ids` | Many2many → `op.subject` | Subjects covered (used for routing) |
| `mentor_ids` | Many2many → `op.mentor` | Approved mentors in this group |
| `student_ids` | Many2many → `op.student` | Enrolled students (when not open to all) |
| `is_open` | Boolean | If `True`, any student can join |
| `question_ids` | One2many → `op.mentorship.message` | Questions posted in this group |

### `op.mentorship.message`

A direct message, a group question, or a group answer.

| Field | Type | Description |
|-------|------|-------------|
| `student_id` | Many2one → `op.student` | Author (student) |
| `mentor_id` | Many2one → `op.mentor` | Recipient (DM) or answering mentor |
| `group_id` | Many2one → `op.mentorship.group` | Group context (for group messages) |
| `subject_id` | Many2one → `op.subject` | Subject / topic of the message |
| `message_type` | Selection | Direct Message / Group Question / Group Answer |
| `state` | Selection | Open → Answered → Closed |
| `subject_line` | Char | Short title/subject |
| `body` | Text | Full message or question text |
| `ai_category_tags` | Char | Comma-separated tags from AI categorisation |
| `parent_id` | Many2one (self) | For threaded replies |
| `reply_ids` | One2many (self) | Replies / answers to this message |

**Validation:**  
- A `direct_message` must have a `mentor_id`.  
- A `group_question` or `group_answer` must have a `group_id`.

**Helper method: `_suggest_mentors_for_question(subject_id)`**  
Returns all approved mentors who list the given subject as an area of expertise.  This is intended to be called by an AI layer or the UI to pre-fill the mentor selector.

---

## User Roles

| Role | Description |
|------|-------------|
| Mentorship User | Can read mentors and groups; can create/edit own messages |
| Mentorship Manager | Full access; can approve/reject mentors; can see all messages |

---

## Menu Structure

```
Mentorship
├── Mentors
├── Groups
├── Direct Messages
├── Group Questions
└── All Messages  (Manager only)
```

---

## Installation

1. Install `openeducat_core` and `mail` (listed as dependencies – `mail` ships with Odoo).
2. Place `openeducat_mentorship` in your Odoo addons directory.
3. Update the app list and install **openEMIS Mentorship**.
4. Assign the **Mentorship Manager** role to guidance counsellors and administrators.
5. Invite mentors to self-register, then approve them via **Mentorship → Mentors**.

---

## Testing

```bash
python odoo-bin -c odoo.conf -d your_db --test-enable -i openeducat_mentorship
```

Tests cover:
- Mentor initial state and approval workflow
- DM validation (mentor required)
- Group question validation (group required)
- Message state transitions (open → answered)

---

## License

LGPL-3.0 – see repository [LICENSE](../LICENSE).
