-- =============================================================================
-- openEMIS – PostgreSQL Direct Seed Script
-- =============================================================================
-- Seeds the openEMIS database with a minimal set of reference data using
-- direct SQL INSERT statements.  Use this script when you want to populate
-- the database without going through the Odoo module installation mechanism
-- (e.g., for quick regression testing or CI/CD pipelines).
--
-- NOTE: This script assumes the Odoo schema (tables, sequences) already
--       exists.  Run it AFTER `odoo --init=openeducat_core ...`.
--
-- Usage:
--   psql -h localhost -U odoo -d openemis -f scripts/seed_postgres.sql
--
-- Or inside the Docker container:
--   docker exec -i openemis_db psql -U odoo -d openemis \
--       -f /mnt/extra-addons/scripts/seed_postgres.sql
-- =============================================================================

\echo '==================================================='
\echo ' openEMIS – Direct PostgreSQL Seed'
\echo '==================================================='

BEGIN;

-- ---------------------------------------------------------------------------
-- Helper: resolve an ir.model.data external ID to an integer primary key.
-- Returns NULL if the XMLID is not found (safe for INSERT … ON CONFLICT).
-- ---------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION openemis_ref(p_module text, p_name text)
RETURNS integer
LANGUAGE plpgsql STABLE AS $$
DECLARE v_id integer;
BEGIN
    SELECT res_id INTO v_id
    FROM ir_model_data
    WHERE module = p_module AND name = p_name
    LIMIT 1;
    RETURN v_id;
END;
$$;

-- ---------------------------------------------------------------------------
-- 1. Ensure a default academic year exists
-- ---------------------------------------------------------------------------
\echo 'Seeding academic year…'

INSERT INTO op_academic_year (name, date_start, date_stop, sequence, active, create_uid, write_uid, create_date, write_date)
SELECT
    '2024-2025',
    '2024-08-01',
    '2025-07-31',
    10,
    true,
    openemis_ref('base','user_root'),
    openemis_ref('base','user_root'),
    now(),
    now()
WHERE NOT EXISTS (
    SELECT 1 FROM op_academic_year WHERE name = '2024-2025'
);

-- ---------------------------------------------------------------------------
-- 2. Ensure a default academic term exists
-- ---------------------------------------------------------------------------
\echo 'Seeding academic term…'

INSERT INTO op_academic_term (
    name, term_type, date_start, date_stop,
    academic_year_id,
    create_uid, write_uid, create_date, write_date
)
SELECT
    'Semester 1 2024-2025',
    'semester',
    '2024-08-01',
    '2024-12-31',
    (SELECT id FROM op_academic_year WHERE name = '2024-2025' LIMIT 1),
    openemis_ref('base','user_root'),
    openemis_ref('base','user_root'),
    now(),
    now()
WHERE NOT EXISTS (
    SELECT 1 FROM op_academic_term WHERE name = 'Semester 1 2024-2025'
);

-- ---------------------------------------------------------------------------
-- 3. Seed sample departments (if not already present)
-- ---------------------------------------------------------------------------
\echo 'Seeding departments…'

DO $$
DECLARE
    dept_names text[] := ARRAY[
        'Computer Science', 'Mathematics', 'Physics',
        'Biology', 'Chemistry', 'English Literature',
        'History', 'Economics', 'Engineering', 'Education'
    ];
    dept_name text;
    company_id integer;
    uid integer;
BEGIN
    SELECT id INTO company_id FROM res_company ORDER BY id LIMIT 1;
    SELECT id INTO uid FROM res_users WHERE login = 'admin' LIMIT 1;
    IF uid IS NULL THEN uid := 1; END IF;

    FOREACH dept_name IN ARRAY dept_names LOOP
        INSERT INTO op_department (name, active, company_id, create_uid, write_uid, create_date, write_date)
        SELECT dept_name, true, company_id, uid, uid, now(), now()
        WHERE NOT EXISTS (SELECT 1 FROM op_department WHERE name = dept_name);
    END LOOP;
END;
$$;

-- ---------------------------------------------------------------------------
-- 4. Seed 20 additional students directly via SQL
--    (Partners first, then op.student rows)
-- ---------------------------------------------------------------------------
\echo 'Seeding 20 additional SQL students…'

DO $$
DECLARE
    i       integer;
    p_id    integer;
    uid     integer;
    cid     integer;
    genders text[] := ARRAY['male','female'];
    bloods  text[] := ARRAY['A+','A-','B+','B-','O+','O-','AB+','AB-'];
    firstnames text[] := ARRAY[
        'Alice','Bob','Carol','David','Eve','Frank','Grace','Henry',
        'Iris','Jack','Kate','Liam','Mia','Noah','Olivia','Paul',
        'Quinn','Rose','Sam','Tina'
    ];
    lastnames text[] := ARRAY[
        'Kamau','Okonkwo','Mensah','Patel','Sharma','Nguyen','Garcia',
        'Martinez','Robinson','Clark','Lewis','Walker','Hall','Allen',
        'Young','Wright','Scott','Torres','Hill','Adams'
    ];
BEGIN
    SELECT id INTO uid FROM res_users WHERE login = 'admin' LIMIT 1;
    IF uid IS NULL THEN uid := 1; END IF;
    SELECT id INTO cid FROM res_company ORDER BY id LIMIT 1;

    FOR i IN 1..20 LOOP
        -- Skip if partner already exists for this seed batch
        IF NOT EXISTS (
            SELECT 1 FROM res_partner
            WHERE email = 'sql_seed_student_' || i || '@openemis.example.com'
        ) THEN
            -- Create partner
            INSERT INTO res_partner (
                name, email, mobile, active, company_type,
                create_uid, write_uid, create_date, write_date
            ) VALUES (
                firstnames[i] || ' SQL ' || lastnames[i],
                'sql_seed_student_' || i || '@openemis.example.com',
                '600000' || lpad(i::text, 4, '0'),
                true,
                'person',
                uid, uid, now(), now()
            ) RETURNING id INTO p_id;

            -- Create student
            INSERT INTO op_student (
                first_name, middle_name, last_name,
                gender, birth_date, blood_group, email,
                active, partner_id,
                create_uid, write_uid, create_date, write_date
            ) VALUES (
                firstnames[i],
                'SQL',
                lastnames[i],
                genders[((i-1) % 2) + 1],
                ('2002-' || lpad(((i % 12)+1)::text, 2, '0') || '-15')::date,
                bloods[((i-1) % 8) + 1],
                'sql_seed_student_' || i || '@openemis.example.com',
                true,
                p_id,
                uid, uid, now(), now()
            );
        END IF;
    END LOOP;
END;
$$;

-- ---------------------------------------------------------------------------
-- 5. Seed 10 additional faculty members via SQL
-- ---------------------------------------------------------------------------
\echo 'Seeding 10 additional SQL faculty members…'

DO $$
DECLARE
    i       integer;
    p_id    integer;
    uid     integer;
    dept_id integer;
    genders text[] := ARRAY['male','female'];
    bloods  text[] := ARRAY['A+','B+','O+','AB+','A-','B-','O-','AB-'];
    firstnames text[] := ARRAY[
        'Prof. James','Dr. Sarah','Prof. Michael','Dr. Lisa',
        'Prof. David','Dr. Emma','Prof. Richard','Dr. Julia',
        'Prof. Thomas','Dr. Helen'
    ];
    lastnames text[] := ARRAY[
        'Anderson','Johnson','Williams','Brown','Davis',
        'Miller','Wilson','Moore','Taylor','Jackson'
    ];
BEGIN
    SELECT id INTO uid FROM res_users WHERE login = 'admin' LIMIT 1;
    IF uid IS NULL THEN uid := 1; END IF;
    SELECT id INTO dept_id FROM op_department ORDER BY id LIMIT 1;

    FOR i IN 1..10 LOOP
        IF NOT EXISTS (
            SELECT 1 FROM res_partner
            WHERE email = 'sql_seed_faculty_' || i || '@openemis.example.com'
        ) THEN
            INSERT INTO res_partner (
                name, email, mobile, active, company_type,
                create_uid, write_uid, create_date, write_date
            ) VALUES (
                firstnames[i] || ' ' || lastnames[i],
                'sql_seed_faculty_' || i || '@openemis.example.com',
                '500000' || lpad(i::text, 4, '0'),
                true,
                'person',
                uid, uid, now(), now()
            ) RETURNING id INTO p_id;

            INSERT INTO op_faculty (
                first_name, last_name,
                gender, birth_date, blood_group, email,
                active, partner_id, main_department_id,
                create_uid, write_uid, create_date, write_date
            ) VALUES (
                firstnames[i],
                lastnames[i],
                genders[((i-1) % 2) + 1],
                ('1975-' || lpad(((i % 12)+1)::text, 2, '0') || '-10')::date,
                bloods[((i-1) % 8) + 1],
                'sql_seed_faculty_' || i || '@openemis.example.com',
                true,
                p_id,
                dept_id,
                uid, uid, now(), now()
            );
        END IF;
    END LOOP;
END;
$$;

-- ---------------------------------------------------------------------------
-- 6. Summary of seeded data
-- ---------------------------------------------------------------------------
\echo ''
\echo '--- Seed Summary ---'

SELECT 'Students'    AS entity, COUNT(*) AS total FROM op_student WHERE active = true
UNION ALL
SELECT 'Faculty'     AS entity, COUNT(*) AS total FROM op_faculty WHERE active = true
UNION ALL
SELECT 'Departments' AS entity, COUNT(*) AS total FROM op_department WHERE active = true
UNION ALL
SELECT 'Academic Years' AS entity, COUNT(*) AS total FROM op_academic_year
UNION ALL
SELECT 'Academic Terms'  AS entity, COUNT(*) AS total FROM op_academic_term
ORDER BY entity;

COMMIT;

\echo ''
\echo '==================================================='
\echo ' Seed complete.'
\echo '==================================================='
