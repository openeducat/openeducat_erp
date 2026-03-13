# openeducat_library – Library Management 📖

## Overview

The **Library** module manages the full lifecycle of physical and digital learning resources in an openEMIS institution.  It covers cataloguing, lending (movements), queuing and access control.

From **openEMIS v18.0** the library has been extended with **CBC learning-resource categorisation**, allowing every item in the catalogue to be tagged with:

* **Grade Level** (Grade 1 – Grade 12 / College / All Grades)
* **Topic** (specific sub-topic within a subject, e.g. "Fractions", "The Water Cycle")
* **Resource Format** (Book, PDF, Video, Audio, Word, Excel/CSV, Image, Presentation, E-Book, Other)

This makes it easy for students to filter the catalogue by their current CBC grade, the subject they are studying and the type of resource they prefer.

---

## Module Structure

```
openeducat_library/
├── __init__.py
├── __manifest__.py
├── demo/                            # Sample media, authors, publishers
├── models/
│   ├── __init__.py
│   ├── author.py                    # op.author
│   ├── media.py                     # op.media  ← extended with CBC fields
│   ├── media_movement.py            # op.media.movement
│   ├── media_queue.py               # op.media.queue
│   ├── media_type.py                # op.media.type
│   ├── media_unit.py                # op.media.unit
│   ├── publisher.py                 # op.publisher
│   └── tag.py                       # op.tag
├── security/
│   ├── ir.model.access.csv
│   └── op_security.xml
└── views/
    ├── media_view.xml               # ← updated with CBC fields
    ├── media_movement_view.xml
    ├── media_queue_view.xml
    ├── media_type_view.xml
    └── ...
```

---

## Key Model: `op.media`

Represents a single catalogued resource (book, video, PDF, etc.).

### Core Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | Char | Title of the resource |
| `isbn` | Char | ISBN code (books) |
| `author_ids` | Many2many → `op.author` | Authors |
| `publisher_ids` | Many2many → `op.publisher` | Publishers |
| `edition` | Char | Edition number |
| `media_type_id` | Many2one → `op.media.type` | Type (book, journal, DVD, …) |
| `course_ids` | Many2many → `op.course` | Relevant courses |
| `subject_ids` | Many2many → `op.subject` | Relevant subjects |
| `tags` | Many2many → `op.tag` | Free-form tags |
| `internal_code` | Char | Library barcode / accession number |
| `unit_ids` | One2many → `op.media.unit` | Physical copies |
| `movement_line` | One2many → `op.media.movement` | Lending history |
| `queue_ids` | One2many → `op.media.queue` | Reservation queue |

### CBC Classification Fields (new in v18.0)

| Field | Type | Description |
|-------|------|-------------|
| `grade_level` | Selection | `all` / `grade_1` … `grade_12` / `college` |
| `topic` | Char | Specific topic (e.g. "Fractions", "Photosynthesis") |
| `resource_format` | Selection | `book` / `pdf` / `word` / `excel` / `video` / `audio` / `image` / `presentation` / `ebook` / `other` |

---

## Resource Formats

| Value | Description |
|-------|-------------|
| `book` | Physical book |
| `pdf` | PDF document |
| `word` | Microsoft Word / LibreOffice Writer document |
| `excel` | Spreadsheet or CSV file |
| `video` | Video lesson or documentary |
| `audio` | Audio lesson, podcast or recording |
| `image` | Image, diagram or infographic |
| `presentation` | Slide deck (PowerPoint / Google Slides) |
| `ebook` | Digital e-book (EPUB/MOBI) |
| `other` | Any other format |

---

## Grade Levels

Resources can be tagged from **Grade 1** through **Grade 12** or **College / University**, or set to **All Grades** when the content is universally applicable (e.g. a dictionary).

---

## Search & Filtering

The media search view now includes:

* **Grade Level** filter/grouping
* **Resource Format** filter/grouping
* Existing filters: Edition, Type, Archived

Students or staff can quickly find, for example, all *video* resources for *Grade 7* on the topic *"Algebra"* by combining these filters.

---

## User Roles

| Role | Access Level |
|------|-------------|
| Student | Read only |
| Library User | Read, borrow, reserve |
| Librarian (Library Manager) | Full access including movements, approvals |

---

## Installation

1. Install `openeducat_core`.
2. Place `openeducat_library` in your Odoo addons directory.
3. Update the app list and install **openEMIS Library**.
4. Configure media types under **Library → Configuration → Media Types**.
5. Add resources via **Library → All Media**.

---

## License

LGPL-3.0 – see repository [LICENSE](../LICENSE).
