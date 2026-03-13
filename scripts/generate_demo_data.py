#!/usr/bin/env python3
"""
openEMIS – Demo Data Generator
================================
Generates Odoo XML demo-data files that populate the database with:
  - 100 classrooms       (openeducat_classroom)
  - 100 staff / faculty  (openeducat_core)
  - 100 parents          (openeducat_parent)
  - 100 students         (openeducat_core, 100 per course/class)

Usage::

    python scripts/generate_demo_data.py

The generated files are written to each module's ``demo/`` directory.
They are referenced by the module manifests and loaded automatically when
Odoo installs the module with demo-data enabled.
"""

import os
import random
import textwrap

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FIRST_NAMES_M = [
    "James", "John", "Robert", "Michael", "William", "David", "Richard",
    "Joseph", "Thomas", "Charles", "Daniel", "Matthew", "Anthony", "Mark",
    "Donald", "Steven", "Paul", "Andrew", "Kenneth", "Joshua", "Kevin",
    "Brian", "George", "Timothy", "Ronald", "Edward", "Jason", "Jeffrey",
    "Ryan", "Jacob", "Gary", "Nicholas", "Eric", "Jonathan", "Stephen",
    "Larry", "Justin", "Scott", "Brandon", "Benjamin", "Samuel", "Frank",
    "Raymond", "Gregory", "Frank", "Alexander", "Patrick", "Jack", "Dennis",
    "Jerry", "Tyler", "Aaron", "Jose", "Adam", "Nathan", "Henry", "Douglas",
    "Zachary", "Peter", "Kyle", "Walter", "Ethan", "Jeremy", "Harold",
    "Terry", "Sean", "Austin", "Gerald", "Keith", "Lawrence", "Noah",
    "Jesse", "Roy", "Joe", "Dylan", "Bryan", "Ralph", "Billy", "Bruce",
    "Carl", "Eugene", "Christian", "Gabriel", "Logan", "Jordan", "Alan",
    "Arthur", "Carlos", "Jesse", "Mason", "Oliver", "Caleb", "Liam",
    "Owen", "Lucas", "Elijah", "Aiden", "Sebastian", "Julian", "Ian",
    "Cole", "Evan", "Isaiah",
]

FIRST_NAMES_F = [
    "Mary", "Patricia", "Jennifer", "Linda", "Barbara", "Elizabeth",
    "Susan", "Jessica", "Sarah", "Karen", "Lisa", "Nancy", "Betty",
    "Margaret", "Sandra", "Ashley", "Dorothy", "Kimberly", "Emily",
    "Donna", "Michelle", "Carol", "Amanda", "Melissa", "Deborah",
    "Stephanie", "Rebecca", "Sharon", "Laura", "Cynthia", "Kathleen",
    "Amy", "Angela", "Shirley", "Anna", "Brenda", "Pamela", "Emma",
    "Nicole", "Helen", "Samantha", "Katherine", "Christine", "Debra",
    "Rachel", "Carolyn", "Janet", "Catherine", "Maria", "Heather",
    "Diane", "Julie", "Joyce", "Victoria", "Kelly", "Christina",
    "Lauren", "Joan", "Evelyn", "Judith", "Olivia", "Martha", "Cheryl",
    "Megan", "Andrea", "Hannah", "Jacqueline", "Frances", "Gloria",
    "Ann", "Teresa", "Kathryn", "Sara", "Janice", "Jean", "Alice",
    "Madison", "Doris", "Abigail", "Julia", "Grace", "Judy", "Natalie",
    "Beverly", "Alexis", "Marie", "Diana", "Brittany", "Danielle",
    "Theresa", "Amber", "Denise", "Marilyn", "Danielle", "Priya",
    "Fatima", "Amina", "Sofia", "Valentina", "Chiara", "Yuki",
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
    "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King",
    "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green",
    "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts", "Parker", "Evans", "Edwards", "Collins", "Stewart",
    "Sanchez", "Morris", "Rogers", "Reed", "Cook", "Morgan", "Bell",
    "Murphy", "Bailey", "Cooper", "Richardson", "Cox", "Howard", "Ward",
    "Torres", "Peterson", "Gray", "Ramirez", "James", "Watson", "Brooks",
    "Kelly", "Sanders", "Price", "Bennett", "Wood", "Barnes", "Ross",
    "Henderson", "Coleman", "Jenkins", "Perry", "Powell", "Long", "Patterson",
    "Hughes", "Flores", "Washington", "Butler", "Simmons", "Foster", "Gonzales",
    "Bryant", "Alexander", "Russell", "Griffin", "Diaz", "Hayes",
    "Patel", "Sharma", "Okonkwo", "Mensah", "Odenyire", "Kamau",
]

MIDDLE_INITIALS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

CITIES = [
    ("New York", "base.state_us_25", "base.us", "10001"),
    ("Los Angeles", "base.state_us_5", "base.us", "90001"),
    ("Chicago", "base.state_us_14", "base.us", "60601"),
    ("Houston", "base.state_us_44", "base.us", "77001"),
    ("Phoenix", "base.state_us_3", "base.us", "85001"),
    ("Philadelphia", "base.state_us_39", "base.us", "19101"),
    ("San Antonio", "base.state_us_44", "base.us", "78201"),
    ("San Diego", "base.state_us_5", "base.us", "92101"),
    ("London", "base.state_uk104", "base.uk", "EC1A 1BB"),
    ("Berlin", "base.state_de_be", "base.de", "10115"),
    ("Paris", "base.state_fr_75", "base.fr", "75001"),
    ("Tokyo", False, "base.jp", "100-0001"),
    ("Nairobi", False, "base.ke", "00100"),
    ("Lagos", False, "base.ng", "100001"),
    ("Cairo", False, "base.eg", "11511"),
    ("Sydney", "base.state_au_nsw", "base.au", "2000"),
    ("Toronto", "base.state_ca_on", "base.ca", "M5H 2N2"),
    ("Mexico City", False, "base.mx", "06600"),
    ("São Paulo", False, "base.br", "01310-100"),
    ("Mumbai", "base.state_in_mh", "base.in", "400001"),
]

BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]

DEPARTMENTS = [
    "openeducat_core.op_department_1",
    "openeducat_core.op_department_2",
    "openeducat_core.op_department_3",
    "openeducat_core.op_department_4",
]

# courses with at least one batch defined
COURSES_WITH_BATCHES = [
    ("openeducat_core.op_course_1", "openeducat_core.op_batch_1"),
    ("openeducat_core.op_course_2", "openeducat_core.op_batch_2"),
    ("openeducat_core.op_course_3", "openeducat_core.op_batch_3"),
    ("openeducat_core.op_course_5", "openeducat_core.op_batch_4"),
    ("openeducat_core.op_course_8", "openeducat_core.op_batch_5"),
    ("openeducat_core.op_course_1", "openeducat_core.op_batch_6"),
    ("openeducat_core.op_course_5", "openeducat_core.op_batch_7"),
    ("openeducat_core.op_course_7", "openeducat_core.op_batch_8"),
    ("openeducat_core.op_course_9", "openeducat_core.op_batch_9"),
    ("openeducat_core.op_course_10", "openeducat_core.op_batch_10"),
]

FACULTY_SUBJECTS = [
    "openeducat_core.op_subject_1",
    "openeducat_core.op_subject_2",
    "openeducat_core.op_subject_5",
    "openeducat_core.op_subject_26",
    "openeducat_core.op_subject_27",
]

PARENT_RELATIONSHIPS = [
    "openeducat_parent.op_parent_relationship_1",  # Father
    "openeducat_parent.op_parent_relationship_2",  # Mother
    "openeducat_parent.op_parent_relationship_3",  # Guardian
]

random.seed(42)  # reproducible


def _pick_gender(i):
    return "f" if i % 2 == 0 else "m"


def _gender_label(i):
    return "female" if i % 2 == 0 else "male"


def _title_ref(i):
    return "base.res_partner_title_miss" if i % 2 == 0 else "base.res_partner_title_mister"


def _first_name(i):
    if i % 2 == 0:
        return FIRST_NAMES_F[i % len(FIRST_NAMES_F)]
    return FIRST_NAMES_M[i % len(FIRST_NAMES_M)]


def _last_name(i):
    return LAST_NAMES[i % len(LAST_NAMES)]


def _middle(i):
    return MIDDLE_INITIALS[i % len(MIDDLE_INITIALS)]


def _birth_year_student(i):
    return 2000 + (i % 8)


def _birth_year_faculty(i):
    return 1975 + (i % 20)


def _birth_year_parent(i):
    return 1965 + (i % 20)


def _city(i):
    return CITIES[i % len(CITIES)]


def _blood(i):
    return BLOOD_GROUPS[i % len(BLOOD_GROUPS)]


def _email(prefix, i):
    fn = _first_name(i).lower()
    ln = _last_name(i).lower()
    return f"{fn}{ln}{prefix}{i:03d}@openemis.example.com"


def _write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    print(f"  written → {os.path.relpath(path, BASE_DIR)}")


# ---------------------------------------------------------------------------
# 1. 100 Classrooms
# ---------------------------------------------------------------------------

def generate_classrooms():
    """Generate 100 classroom records for openeducat_classroom."""
    lines = ['<?xml version="1.0" encoding="utf-8"?>', '<odoo noupdate="1">']
    num_courses = 59  # courses 1..59 exist per op.course.csv (60 rows incl. header)
    for i in range(1, 101):
        course_num = ((i - 1) % num_courses) + 1
        lines.append(f'''    <record id="op_classroom_bulk_{i:03d}" model="op.classroom">
        <field name="code">CR{i:03d}</field>
        <field name="name">Classroom {i:03d}</field>
        <field name="capacity">30</field>
        <field name="course_id" ref="openeducat_core.op_course_{course_num}"/>
    </record>''')
    lines.append('</odoo>\n')
    path = os.path.join(BASE_DIR, "openeducat_classroom", "demo",
                        "openemis_classrooms_bulk.xml")
    _write(path, "\n".join(lines))


# ---------------------------------------------------------------------------
# 2. 100 Faculty / Staff
# ---------------------------------------------------------------------------

def generate_faculty():
    """Generate 100 faculty partner + faculty records for openeducat_core."""
    # Partners start from op_res_partner_bulk_f_1
    partner_lines = ['<?xml version="1.0" encoding="utf-8"?>', '<odoo noupdate="1">']
    faculty_lines = ['<?xml version="1.0" encoding="utf-8"?>', '<odoo noupdate="1">']

    for i in range(1, 101):
        fn = _first_name(i + 3)   # offset to avoid collisions with student names
        mn = _middle(i)
        ln = _last_name(i + 7)
        email = _email("fac", i)
        mobile = f"9{i:09d}"
        city, state_ref, country_ref, zipcode = _city(i)
        dept = DEPARTMENTS[i % len(DEPARTMENTS)]
        subj1 = FACULTY_SUBJECTS[i % len(FACULTY_SUBJECTS)]
        subj2 = FACULTY_SUBJECTS[(i + 1) % len(FACULTY_SUBJECTS)]

        partner_lines.append(f'''    <record id="op_res_partner_bulk_f_{i:03d}" model="res.partner">
        <field name="name">{fn} {mn} {ln}</field>
        <field name="mobile">{mobile}</field>
        <field name="email">{email}</field>
    </record>''')

        city_field = f'<field name="city">{city}</field>'
        state_field = (f'<field name="state_id" ref="{state_ref}"/>'
                       if state_ref else '')
        country_field = f'<field name="country_id" ref="{country_ref}"/>'

        faculty_lines.append(f'''    <record id="op_faculty_bulk_{i:03d}" model="op.faculty">
        <field name="title" ref="{_title_ref(i + 3)}"/>
        <field name="first_name">{fn}</field>
        <field name="middle_name">{mn}</field>
        <field name="last_name">{ln}</field>
        <field name="gender">{_gender_label(i + 3)}</field>
        <field name="birth_date">{_birth_year_faculty(i)}-{(i % 12) + 1:02d}-{(i % 28) + 1:02d}</field>
        <field name="blood_group">{_blood(i)}</field>
        <field name="email">{email}</field>
        {city_field}
        <field name="zip">{zipcode}</field>
        {state_field}
        {country_field}
        <field name="type">contact</field>
        <field name="active">True</field>
        <field name="partner_id" ref="op_res_partner_bulk_f_{i:03d}"/>
        <field name="main_department_id" ref="{dept}"/>
        <field name="faculty_subject_ids" eval="[(4,ref('{subj1}')),(4,ref('{subj2}'))]"/>
    </record>''')

    partner_lines.append('</odoo>\n')
    faculty_lines.append('</odoo>\n')

    _write(os.path.join(BASE_DIR, "openeducat_core", "demo",
                        "openemis_faculty_bulk_partners.xml"),
           "\n".join(partner_lines))
    _write(os.path.join(BASE_DIR, "openeducat_core", "demo",
                        "openemis_faculty_bulk.xml"),
           "\n".join(faculty_lines))


# ---------------------------------------------------------------------------
# 3. 100 Parents
# ---------------------------------------------------------------------------

def generate_parents():
    """Generate 100 parent partner + user + parent records for openeducat_parent."""
    partner_lines = ['<?xml version="1.0" encoding="utf-8"?>', '<odoo noupdate="1">']
    user_lines = ['<?xml version="1.0" encoding="utf-8"?>', '<odoo noupdate="1">']
    parent_lines = ['<?xml version="1.0" encoding="utf-8"?>', '<odoo noupdate="1">']

    for i in range(1, 101):
        fn = _first_name(i + 1)
        mn = _middle(i + 2)
        ln = _last_name(i + 3)
        email = _email("par", i)
        mobile = f"8{i:09d}"
        login = f"parent_bulk_{i:03d}@openemis.example.com"
        rel = PARENT_RELATIONSHIPS[i % len(PARENT_RELATIONSHIPS)]
        # link this parent to two students that were created in the students block
        stud_a = ((i - 1) % 100) + 1
        stud_b = (i % 100) + 1

        partner_lines.append(f'''    <record id="op_res_partner_bulk_p_{i:03d}" model="res.partner">
        <field name="name">{fn} {mn} {ln}</field>
        <field name="email">{email}</field>
        <field name="mobile">{mobile}</field>
    </record>''')

        user_lines.append(f'''    <record id="op_user_parent_bulk_{i:03d}" model="res.users">
        <field name="login">{login}</field>
        <field name="password">parent123</field>
        <field name="tz">UTC</field>
        <field name="is_parent">True</field>
        <field name="partner_id" ref="op_res_partner_bulk_p_{i:03d}"/>
        <field name="company_id" ref="base.main_company"/>
        <field name="groups_id" eval="[(4, ref('base.group_portal'))]"/>
    </record>''')

        parent_lines.append(f'''    <record id="op_parent_bulk_{i:03d}" model="op.parent">
        <field name="name" ref="openeducat_parent.op_res_partner_bulk_p_{i:03d}"/>
        <field name="student_ids" eval="[(6,0,[ref('openeducat_core.op_student_bulk_{stud_a:03d}'),ref('openeducat_core.op_student_bulk_{stud_b:03d}')])]"/>
        <field name="relationship_id" ref="{rel}"/>
        <field name="user_id" ref="openeducat_parent.op_user_parent_bulk_{i:03d}"/>
    </record>''')

    partner_lines.append('</odoo>\n')
    user_lines.append('</odoo>\n')
    parent_lines.append('</odoo>\n')

    _write(os.path.join(BASE_DIR, "openeducat_parent", "demo",
                        "openemis_parent_bulk_partners.xml"),
           "\n".join(partner_lines))
    _write(os.path.join(BASE_DIR, "openeducat_parent", "demo",
                        "openemis_parent_bulk_users.xml"),
           "\n".join(user_lines))
    _write(os.path.join(BASE_DIR, "openeducat_parent", "demo",
                        "openemis_parent_bulk.xml"),
           "\n".join(parent_lines))


# ---------------------------------------------------------------------------
# 4. 100 Students (per class – 100 students mapped across 10 courses/batches)
# ---------------------------------------------------------------------------

def generate_students():
    """Generate 100 student partner + student records for openeducat_core.

    Each student is enrolled in a course/batch drawn from COURSES_WITH_BATCHES
    so every class gets exactly 10 students (10 courses × 10 students = 100).
    """
    partner_lines = ['<?xml version="1.0" encoding="utf-8"?>', '<odoo noupdate="1">']
    student_lines = ['<?xml version="1.0" encoding="utf-8"?>', '<odoo noupdate="1">']
    course_lines = ['<?xml version="1.0" encoding="utf-8"?>', '<odoo noupdate="1">']

    for i in range(1, 101):
        fn = _first_name(i)
        mn = _middle(i)
        ln = _last_name(i)
        gender = _pick_gender(i)
        email = _email("stu", i)
        mobile = f"7{i:09d}"
        city, state_ref, country_ref, zipcode = _city(i)
        blood = _blood(i)
        birth = (f"{_birth_year_student(i)}-"
                 f"{(i % 12) + 1:02d}-"
                 f"{(i % 28) + 1:02d}")

        partner_lines.append(f'''    <record id="op_res_partner_bulk_s_{i:03d}" model="res.partner">
        <field name="name">{fn} {mn} {ln}</field>
        <field name="mobile">{mobile}</field>
        <field name="email">{email}</field>
    </record>''')

        city_field = f'<field name="city">{city}</field>'
        state_field = (f'<field name="state_id" ref="{state_ref}"/>'
                       if state_ref else '')
        country_field = f'<field name="country_id" ref="{country_ref}"/>'

        student_lines.append(f'''    <record id="op_student_bulk_{i:03d}" model="op.student">
        <field name="title" ref="{_title_ref(i)}"/>
        <field name="first_name">{fn}</field>
        <field name="middle_name">{mn}</field>
        <field name="last_name">{ln}</field>
        <field name="gender">{gender}</field>
        <field name="birth_date">{birth}</field>
        <field name="blood_group">{blood}</field>
        <field name="email">{email}</field>
        {city_field}
        <field name="zip">{zipcode}</field>
        {state_field}
        {country_field}
        <field name="type">contact</field>
        <field name="active">True</field>
        <field name="partner_id" ref="op_res_partner_bulk_s_{i:03d}"/>
    </record>''')

        course_ref, batch_ref = COURSES_WITH_BATCHES[(i - 1) % len(COURSES_WITH_BATCHES)]
        course_lines.append(f'''    <record id="op_student_course_bulk_{i:03d}" model="op.student.course">
        <field name="student_id" ref="op_student_bulk_{i:03d}"/>
        <field name="course_id" ref="{course_ref}"/>
        <field name="batch_id" ref="{batch_ref}"/>
    </record>''')

    partner_lines.append('</odoo>\n')
    student_lines.append('</odoo>\n')
    course_lines.append('</odoo>\n')

    _write(os.path.join(BASE_DIR, "openeducat_core", "demo",
                        "openemis_student_bulk_partners.xml"),
           "\n".join(partner_lines))
    _write(os.path.join(BASE_DIR, "openeducat_core", "demo",
                        "openemis_student_bulk.xml"),
           "\n".join(student_lines))
    _write(os.path.join(BASE_DIR, "openeducat_core", "demo",
                        "openemis_student_course_bulk.xml"),
           "\n".join(course_lines))


# ---------------------------------------------------------------------------
# 5. Update manifests to include new demo files
# ---------------------------------------------------------------------------

def _insert_demo_entry(manifest_path, new_entry, anchor):
    """Insert *new_entry* after *anchor* line inside the 'demo' list."""
    with open(manifest_path, encoding="utf-8") as fh:
        content = fh.read()
    if new_entry in content:
        return  # already present
    idx = content.find(anchor)
    if idx == -1:
        print(f"  WARNING: anchor not found in {manifest_path}: {anchor!r}")
        return
    insert_at = idx + len(anchor)
    content = content[:insert_at] + "\n        " + new_entry + "," + content[insert_at:]
    with open(manifest_path, "w", encoding="utf-8") as fh:
        fh.write(content)
    print(f"  patched manifest → {os.path.relpath(manifest_path, BASE_DIR)}")


def patch_manifests():
    """Add new demo data files to relevant manifests."""
    # openeducat_core
    core_manifest = os.path.join(BASE_DIR, "openeducat_core", "__manifest__.py")
    for entry, anchor in [
        ("'demo/openemis_student_bulk_partners.xml'",
         "'demo/res_partner_demo.xml'"),
        ("'demo/openemis_student_bulk.xml'",
         "'demo/student_demo.xml'"),
        ("'demo/openemis_student_course_bulk.xml'",
         "'demo/student_course_demo.xml'"),
        ("'demo/openemis_faculty_bulk_partners.xml'",
         "'demo/res_partner_demo.xml'"),
        ("'demo/openemis_faculty_bulk.xml'",
         "'demo/faculty_demo.xml'"),
    ]:
        _insert_demo_entry(core_manifest, entry, anchor)

    # openeducat_classroom
    classroom_manifest = os.path.join(BASE_DIR, "openeducat_classroom",
                                      "__manifest__.py")
    _insert_demo_entry(classroom_manifest,
                       "'demo/openemis_classrooms_bulk.xml'",
                       "'demo/classroom_demo.xml'")

    # openeducat_parent
    parent_manifest = os.path.join(BASE_DIR, "openeducat_parent", "__manifest__.py")
    for entry, anchor in [
        ("'demo/openemis_parent_bulk_partners.xml'",
         "'demo/res_partner_demo.xml'"),
        ("'demo/openemis_parent_bulk_users.xml'",
         "'demo/res_users_demo.xml'"),
        ("'demo/openemis_parent_bulk.xml'",
         "'demo/parent_demo.xml'"),
    ]:
        _insert_demo_entry(parent_manifest, entry, anchor)


# ---------------------------------------------------------------------------
# Entry-point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("openEMIS – generating bulk demo data …\n")

    print("1/4  Classrooms …")
    generate_classrooms()

    print("2/4  Faculty / Staff …")
    generate_faculty()

    print("3/4  Students …")
    generate_students()

    print("4/4  Parents …")
    generate_parents()

    print("\nPatching module manifests …")
    patch_manifests()

    print("\n✓  Done.  Re-install the affected Odoo modules with demo data to load the records.")
