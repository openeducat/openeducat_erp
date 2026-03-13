# openeducat_digiguide – DigiGuide: Digital Career Guidance 🎯

## Overview

**DigiGuide** is the Digital Career Guidance module for openEMIS.  It consumes incremental CBC (Competency-Based Curriculum) academic performance data that accumulates from Grade 1 through Grade 12 and college, and uses it to:

1. **Predict** likely national examination performance for key milestone grades.
2. **Integrate** with the KUCCPS (Kenya Universities and Colleges Central Placement Service) API to fetch current university and college programme requirements.
3. **Match** each student's predicted performance and subject combination against KUCCPS career entry requirements.

This allows guidance counsellors, teachers and parents to have an early view of where a student is headed academically – and to intervene or celebrate well before the national exams arrive.

---

## Kenya CBC Context

Under Kenya's Competency-Based Curriculum (CBC), students progress through three main bands:

| Band | Grades | National Exam |
|------|--------|---------------|
| Lower Primary | 1 – 3 | **Grade 3 Assessment** |
| Upper Primary | 4 – 6 | **Grade 6 Kenya Primary School Education Assessment (KPSEA)** |
| Junior Secondary | 7 – 9 | **Grade 9 Junior Secondary Assessment** |
| Senior Secondary | 10 – 12 | **Grade 12 Kenya Certificate of Secondary Education (KCSE)** |

For each national exam, DigiGuide aggregates the relevant continuous-assessment scores (weekly assignments, mid-term, termly and end-of-year exams) from the preceding grades and calculates a weighted-average prediction.

---

## Module Structure

```
openeducat_digiguide/
├── __init__.py
├── __manifest__.py
├── data/
│   └── digiguide_data.xml          # KUCCPS API system parameter defaults
├── demo/
│   ├── academic_performance_demo.xml
│   └── kuccps_career_demo.xml      # 5 sample KUCCPS programmes
├── menus/
│   └── op_menu.xml
├── models/
│   ├── __init__.py
│   ├── academic_performance.py     # op.academic.performance
│   ├── national_exam_prediction.py # op.national.exam.prediction
│   ├── kuccps_career.py            # op.kuccps.career + KUCCPS API sync
│   └── career_match.py             # op.career.match
├── security/
│   ├── ir.model.access.csv
│   └── op_security.xml
├── tests/
│   ├── __init__.py
│   └── test_digiguide.py
└── views/
    ├── academic_performance_view.xml
    ├── career_match_view.xml
    ├── kuccps_career_view.xml
    └── national_exam_prediction_view.xml
```

---

## Models

### `op.academic.performance`

Records a single assessment score for a student.

| Field | Type | Description |
|-------|------|-------------|
| `student_id` | Many2one → `op.student` | The student being assessed |
| `subject_id` | Many2one → `op.subject` | Subject assessed |
| `academic_year` | Char | e.g. `2024` |
| `grade` | Selection | Grade 1 – Grade 12 |
| `term` | Selection | Term 1 / Term 2 / Term 3 |
| `assessment_type` | Selection | Weekly Assignment / Mid Term / Termly / Annual |
| `score` | Float | Raw score |
| `max_score` | Float | Total marks available (default 100) |
| `percentage` | Float (computed) | `(score / max_score) × 100` |
| `grade_letter` | Char (computed) | A / B / C / D / E |
| `is_national_exam_grade` | Boolean | Flag for official national exam scores |

### `op.national.exam.prediction`

Holds a predicted national-exam score derived from historical performance data.

| Field | Type | Description |
|-------|------|-------------|
| `student_id` | Many2one | Student |
| `national_exam_grade` | Selection | Grade 3 / 6 / 9 / 12 |
| `predicted_percentage` | Float | Weighted-average prediction |
| `predicted_grade_letter` | Char (computed) | A–E |
| `confidence_level` | Float | Statistical confidence (capped at 95 %) |
| `state` | Selection | Draft → Computed → Confirmed |
| `performance_ids` | Many2many | Source performance records used |

**Action: `action_compute_prediction`**  
Fetches all `op.academic.performance` records for the relevant grades and computes a simple weighted average.  Confidence increases with the number of available data points (50 % + 2 % per record, capped at 95 %).

### `op.kuccps.career`

Stores a career/programme fetched from the KUCCPS API or entered manually.

| Field | Type | Description |
|-------|------|-------------|
| `name` | Char | Programme name |
| `kuccps_code` | Char | Unique KUCCPS code |
| `minimum_grade` | Char | Minimum overall grade (e.g. C+) |
| `minimum_points` | Float | Minimum cluster points required |
| `required_subjects` | Text | Subject combination requirements |
| `institution_name` | Char | University or college name |
| `institution_type` | Selection | University / College–TVET |
| `sync_status` | Selection | Pending / Synced / Error |

**Action: `action_sync_from_kuccps`**  
Calls `GET {kuccps_api_url}/programmes` with a Bearer token (configured via `Settings → Technical → System Parameters`).  Upserts records based on `kuccps_code`.

> **Configuration**
> | Parameter | Key | Default |
> |-----------|-----|---------|
> | API Base URL | `digiguide.kuccps_api_url` | `https://api.kuccps.net/v1` |
> | API Key | `digiguide.kuccps_api_key` | *(empty)* |

### `op.career.match`

Links a student's prediction to a KUCCPS career and records suitability.

| Field | Type | Description |
|-------|------|-------------|
| `student_id` | Many2one | Student |
| `career_id` | Many2one | KUCCPS career |
| `prediction_id` | Many2one | Source prediction |
| `match_status` | Selection | Not Evaluated / Eligible / Conditionally Eligible / Not Eligible |
| `match_score` | Float | How well the student meets requirements (%) |

**Action: `action_evaluate_match`**  
Compares `predicted_percentage` to `minimum_points`.  A student scoring ≥ 100 % of the requirement is **Eligible**; ≥ 85 % is **Conditionally Eligible**; below that is **Not Eligible**.

---

## User Roles

| Role | Create | Edit | Delete | KUCCPS Sync |
|------|--------|------|--------|-------------|
| DigiGuide User | ✗ | ✗ | ✗ | ✗ |
| DigiGuide Manager | ✓ | ✓ | ✓ | ✓ |

---

## Installation

1. Install `openeducat_exam` and `openeducat_assignment` (listed as dependencies).
2. Place the `openeducat_digiguide` folder in your Odoo addons directory.
3. Update the app list and install **openEMIS DigiGuide**.
4. Go to **Settings → Technical → System Parameters** and set:
   - `digiguide.kuccps_api_url` – base URL of the KUCCPS REST API.
   - `digiguide.kuccps_api_key` – API key or Bearer token.
5. Click **Configuration → KUCCPS Careers → Sync from KUCCPS API** to import career data.

---

## Testing

```bash
python odoo-bin -c odoo.conf -d your_db --test-enable -i openeducat_digiguide
```

Tests cover:
- Percentage computation and grade letter derivation
- National exam prediction algorithm
- Career match eligibility thresholds

---

## License

LGPL-3.0 – see repository [LICENSE](../LICENSE).
