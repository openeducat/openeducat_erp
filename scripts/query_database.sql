-- =============================================================================
-- openEMIS – PostgreSQL Seed / Verification Queries
-- =============================================================================
-- This file contains SQL queries for:
--   1. Inspecting the openEMIS schema and data after Odoo initialisation.
--   2. Verifying that demo data was loaded correctly.
--   3. Useful analytics / reporting queries for the database.
--
-- Run against the openEMIS database:
--   psql -h localhost -U odoo -d openemis -f scripts/query_database.sql
--
-- Or inside the Docker container:
--   docker exec -i openemis_db psql -U odoo -d openemis \
--       -f /mnt/extra-addons/scripts/query_database.sql
-- =============================================================================

\echo '==================================================='
\echo ' openEMIS – Database Verification Queries'
\echo '==================================================='

-- ---------------------------------------------------------------------------
-- 1. Record counts for core entities
-- ---------------------------------------------------------------------------
\echo ''
\echo '--- Record Counts ---'

SELECT 'Students'    AS entity, COUNT(*) AS total FROM op_student WHERE active = true
UNION ALL
SELECT 'Faculty'     AS entity, COUNT(*) AS total FROM op_faculty WHERE active = true
UNION ALL
SELECT 'Courses'     AS entity, COUNT(*) AS total FROM op_course WHERE active = true
UNION ALL
SELECT 'Batches'     AS entity, COUNT(*) AS total FROM op_batch WHERE active = true
UNION ALL
SELECT 'Subjects'    AS entity, COUNT(*) AS total FROM op_subject WHERE active = true
UNION ALL
SELECT 'Departments' AS entity, COUNT(*) AS total FROM op_department WHERE active = true
ORDER BY entity;

-- ---------------------------------------------------------------------------
-- 2. Classrooms
-- ---------------------------------------------------------------------------
\echo ''
\echo '--- Classrooms (first 10) ---'

SELECT
    c.code,
    c.name,
    c.capacity,
    co.name AS course
FROM op_classroom c
LEFT JOIN op_course co ON co.id = c.course_id
ORDER BY c.code
LIMIT 10;

-- ---------------------------------------------------------------------------
-- 3. Students – top 10 (alphabetical)
-- ---------------------------------------------------------------------------
\echo ''
\echo '--- Students (first 10) ---'

SELECT
    s.gr_no,
    s.first_name,
    s.middle_name,
    s.last_name,
    s.gender,
    s.birth_date,
    s.blood_group
FROM op_student s
ORDER BY s.last_name, s.first_name
LIMIT 10;

-- ---------------------------------------------------------------------------
-- 4. Faculty – top 10
-- ---------------------------------------------------------------------------
\echo ''
\echo '--- Faculty (first 10) ---'

SELECT
    f.first_name,
    f.middle_name,
    f.last_name,
    f.gender,
    d.name AS department
FROM op_faculty f
LEFT JOIN op_department d ON d.id = f.main_department_id
ORDER BY f.last_name, f.first_name
LIMIT 10;

-- ---------------------------------------------------------------------------
-- 5. Student course enrolments
-- ---------------------------------------------------------------------------
\echo ''
\echo '--- Student–Course Enrolments (first 10) ---'

SELECT
    s.first_name || ' ' || s.last_name AS student,
    co.name AS course,
    b.name  AS batch
FROM op_student_course sc
JOIN op_student s  ON s.id  = sc.student_id
JOIN op_course  co ON co.id = sc.course_id
LEFT JOIN op_batch b ON b.id = sc.batch_id
ORDER BY student
LIMIT 10;

-- ---------------------------------------------------------------------------
-- 6. Academic years and terms
-- ---------------------------------------------------------------------------
\echo ''
\echo '--- Academic Years ---'

SELECT name, date_start, date_stop, sequence
FROM op_academic_year
ORDER BY sequence;

\echo ''
\echo '--- Academic Terms ---'

SELECT name, date_start, date_stop, academic_year_id
FROM op_academic_term
ORDER BY date_start;

-- ---------------------------------------------------------------------------
-- 7. Courses and their batch counts
-- ---------------------------------------------------------------------------
\echo ''
\echo '--- Courses with Batch Counts ---'

SELECT
    co.name                       AS course,
    co.no_of_years,
    COUNT(b.id)                   AS batch_count,
    COALESCE(SUM(sc.student_cnt), 0) AS enrolled_students
FROM op_course co
LEFT JOIN op_batch b ON b.course_id = co.id
LEFT JOIN (
    SELECT course_id, COUNT(*) AS student_cnt
    FROM op_student_course
    GROUP BY course_id
) sc ON sc.course_id = co.id
WHERE co.active = true
GROUP BY co.name, co.no_of_years
ORDER BY enrolled_students DESC
LIMIT 20;

-- ---------------------------------------------------------------------------
-- 8. Blood group distribution among students
-- ---------------------------------------------------------------------------
\echo ''
\echo '--- Student Blood Group Distribution ---'

SELECT
    blood_group,
    COUNT(*) AS student_count,
    ROUND(100.0 * COUNT(*) / NULLIF(SUM(COUNT(*)) OVER (), 0), 1) AS pct
FROM op_student
WHERE active = true AND blood_group IS NOT NULL
GROUP BY blood_group
ORDER BY student_count DESC;

-- ---------------------------------------------------------------------------
-- 9. Gender breakdown
-- ---------------------------------------------------------------------------
\echo ''
\echo '--- Gender Breakdown (Students) ---'

SELECT
    gender,
    COUNT(*) AS total
FROM op_student
WHERE active = true
GROUP BY gender
ORDER BY total DESC;

-- ---------------------------------------------------------------------------
-- 10. Installed Odoo modules (openEMIS)
-- ---------------------------------------------------------------------------
\echo ''
\echo '--- Installed openEMIS Modules ---'

SELECT name, state, author, latest_version
FROM ir_module_module
WHERE name LIKE 'openeducat%' AND state = 'installed'
ORDER BY name;

\echo ''
\echo '==================================================='
\echo ' Verification complete.'
\echo '==================================================='
