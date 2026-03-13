# openeducat_blog – Educational Blog ✍️

## Overview

The **Blog** module provides a curated educational publishing platform within openEMIS where mentors, teachers, parents and professionals can write and publish articles that all students can read.

Key capabilities:

* **Rich article authoring** with HTML content, cover images, attachments and keyword tags.
* **Category hierarchy** for organising posts by educational theme, subject or grade level.
* **Grade-level and subject tagging** so students quickly find content relevant to their CBC level.
* **Comment system with moderation** – students can post comments which are held for approval before becoming visible.
* **Content lifecycle** – Draft → Under Review → Published → Archived.
* **Role-based access** – Readers, Authors (write their own posts) and Managers (publish/moderate).

---

## Module Structure

```
openeducat_blog/
├── __init__.py
├── __manifest__.py
├── demo/
│   ├── blog_category_demo.xml      # STEM, Career Guidance, Health, Arts
│   └── blog_post_demo.xml          # 2 sample published articles
├── menus/
│   └── op_menu.xml
├── models/
│   ├── __init__.py
│   ├── blog_category.py            # op.blog.category
│   ├── blog_post.py                # op.blog.post
│   └── blog_comment.py             # op.blog.comment
├── security/
│   ├── ir.model.access.csv
│   └── op_security.xml
├── tests/
│   ├── __init__.py
│   └── test_blog.py
└── views/
    ├── blog_category_view.xml
    ├── blog_comment_view.xml
    └── blog_post_view.xml
```

---

## Models

### `op.blog.category`

Hierarchical grouping for blog posts.

| Field | Type | Description |
|-------|------|-------------|
| `name` | Char | Category name (e.g. "STEM", "Career Guidance") |
| `description` | Text | What this category covers |
| `parent_id` | Many2one (self) | Parent category for nesting |
| `child_ids` | One2many (self) | Sub-categories |
| `post_count` | Integer (computed) | Number of published posts in this category |

### `op.blog.post`

An educational article.

| Field | Type | Description |
|-------|------|-------------|
| `name` | Char | Article title |
| `slug` | Char | URL-friendly short title (auto-generated from title) |
| `author_id` | Many2one → `res.partner` | Author (defaults to current user's partner) |
| `author_type` | Selection | Mentor / Teacher / Parent / Professional / Administrator |
| `category_ids` | Many2many → `op.blog.category` | Categories the post belongs to |
| `subject_ids` | Many2many → `op.subject` | Related CBC subjects |
| `grade_level` | Selection | Target CBC grade level (All / Grade 1–12 / College) |
| `tags` | Char | Comma-separated keyword tags |
| `summary` | Text | Short excerpt shown in listings |
| `body` | Html | Full article content (sanitised) |
| `cover_image` | Binary | Cover/thumbnail image |
| `state` | Selection | Draft → Under Review → Published → Archived |
| `publish_date` | Datetime | Set automatically when publishing |
| `view_count` | Integer | Incremented via `action_increment_views` |
| `allow_comments` | Boolean | Whether students may comment |

**Lifecycle actions:**  
`action_submit_review` → `action_publish` (Manager only) → `action_archive_post`  
`action_reset_draft` – return any post to Draft.

**Validation:** `slug` must be unique across all posts.

### `op.blog.comment`

A comment left on a published post.

| Field | Type | Description |
|-------|------|-------------|
| `post_id` | Many2one → `op.blog.post` | Post being commented on |
| `author_id` | Many2one → `res.partner` | Commenter |
| `body` | Text | Comment text |
| `state` | Selection | Pending Moderation → Approved / Rejected |
| `parent_id` | Many2one (self) | For nested replies |

**Validation:** Raises a `UserError` if `allow_comments` is `False` on the linked post.  
**Moderation actions:** `action_approve`, `action_reject`

---

## User Roles

| Role | Can Read | Can Author | Can Publish | Can Moderate Comments |
|------|----------|------------|-------------|----------------------|
| Reader | ✓ Published only | ✗ | ✗ | ✗ |
| Author | ✓ | ✓ own posts | ✗ | ✗ |
| Manager | ✓ all | ✓ | ✓ | ✓ |

---

## Menu Structure

```
Blog
├── Articles           (published posts – all roles)
├── My Posts           (author drafts & submissions – Author + Manager)
├── All Posts          (Manager only)
├── Moderate Comments  (pending comments – Manager only)
└── Configuration
    └── Categories
```

---

## Installation

1. Install `openeducat_core` and `mail`.
2. Place `openeducat_blog` in your Odoo addons directory.
3. Update the app list and install **openEMIS Blog**.
4. Assign **Blog Manager** to content administrators.
5. Assign **Blog Author** to teachers, mentors and parents who will write articles.
6. All other users receive **Blog Reader** access automatically.

---

## Testing

```bash
python odoo-bin -c odoo.conf -d your_db --test-enable -i openeducat_blog
```

Tests cover:
- Full post lifecycle (draft → review → published)
- Automatic slug generation from title
- Unique-slug constraint enforcement
- Comment moderation workflow
- Comment-disabled enforcement

---

## License

LGPL-3.0 – see repository [LICENSE](../LICENSE).
