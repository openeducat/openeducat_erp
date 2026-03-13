###############################################################################
#
#    openEMIS
#    Copyright (C) 2009-TODAY openEMIS(<https://www.openemis.org>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

"""
openEMIS – Branding & Bulk Data Regression Tests
=================================================
Tests that validate:
  1. Module manifests carry openEMIS branding (name, author, website).
  2. The data-generation script produces valid XML fixture files.
  3. Core models (student, faculty, classroom, parent) can be created and
     queried, providing a functional smoke-test for end-to-end integration.
"""

import ast
import os
import xml.etree.ElementTree as ET

from odoo.tests import TransactionCase

BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..")


class TestOpenEMISBranding(TransactionCase):
    """Validate openEMIS branding in all module manifests."""

    # Manifests that must carry openEMIS branding
    MANIFEST_PATHS = [
        "openeducat_core/__manifest__.py",
        "openeducat_erp/__manifest__.py",
        "openeducat_classroom/__manifest__.py",
        "openeducat_fees/__manifest__.py",
        "openeducat_exam/__manifest__.py",
        "openeducat_activity/__manifest__.py",
        "openeducat_library/__manifest__.py",
        "openeducat_parent/__manifest__.py",
        "openeducat_assignment/__manifest__.py",
        "openeducat_attendance/__manifest__.py",
        "openeducat_facility/__manifest__.py",
        "openeducat_timetable/__manifest__.py",
        "openeducat_admission/__manifest__.py",
        "theme_web_openeducat/__manifest__.py",
    ]

    def _load_manifest(self, rel_path):
        """Parse and return the manifest dict for *rel_path*."""
        abs_path = os.path.join(BASE_DIR, rel_path)
        with open(abs_path, encoding="utf-8") as fh:
            src = fh.read()
        # Strip the comment header (lines starting with #) before eval
        lines = [l for l in src.splitlines() if not l.startswith("#")]
        return ast.literal_eval("\n".join(lines))

    def test_manifest_author_is_openemis(self):
        """Every manifest must list 'openEMIS' as the author."""
        for rel in self.MANIFEST_PATHS:
            manifest = self._load_manifest(rel)
            author = manifest.get("author", "")
            self.assertIn(
                "openEMIS",
                author,
                f"Manifest {rel}: expected 'openEMIS' in author, got {author!r}",
            )

    def test_manifest_website_is_openemis(self):
        """Every manifest must point at the openEMIS website."""
        for rel in self.MANIFEST_PATHS:
            manifest = self._load_manifest(rel)
            website = manifest.get("website", "")
            self.assertIn(
                "openemis",
                website.lower(),
                f"Manifest {rel}: expected openemis URL, got {website!r}",
            )

    def test_manifest_name_contains_openemis(self):
        """Every module name must start with 'openEMIS'."""
        for rel in self.MANIFEST_PATHS:
            manifest = self._load_manifest(rel)
            name = manifest.get("name", "")
            self.assertTrue(
                name.lower().startswith("openemis"),
                f"Manifest {rel}: expected name starting with 'openEMIS', got {name!r}",
            )

    def test_no_openeducat_branding_in_manifest_name(self):
        """Module names must not contain legacy 'OpenEduCat' string."""
        for rel in self.MANIFEST_PATHS:
            manifest = self._load_manifest(rel)
            name = manifest.get("name", "")
            self.assertNotIn(
                "OpenEduCat",
                name,
                f"Manifest {rel}: legacy 'OpenEduCat' found in name: {name!r}",
            )


class TestBulkDemoDataFiles(TransactionCase):
    """Validate that all bulk demo XML files are present and well-formed."""

    BULK_XML_FILES = [
        "openeducat_classroom/demo/openemis_classrooms_bulk.xml",
        "openeducat_core/demo/openemis_faculty_bulk_partners.xml",
        "openeducat_core/demo/openemis_faculty_bulk.xml",
        "openeducat_core/demo/openemis_student_bulk_partners.xml",
        "openeducat_core/demo/openemis_student_bulk.xml",
        "openeducat_core/demo/openemis_student_course_bulk.xml",
        "openeducat_parent/demo/openemis_parent_bulk_partners.xml",
        "openeducat_parent/demo/openemis_parent_bulk_users.xml",
        "openeducat_parent/demo/openemis_parent_bulk.xml",
    ]

    # Expected record count per file
    EXPECTED_COUNTS = {
        "openemis_classrooms_bulk.xml": 100,
        "openemis_faculty_bulk_partners.xml": 100,
        "openemis_faculty_bulk.xml": 100,
        "openemis_student_bulk_partners.xml": 100,
        "openemis_student_bulk.xml": 100,
        "openemis_student_course_bulk.xml": 100,
        "openemis_parent_bulk_partners.xml": 100,
        "openemis_parent_bulk_users.xml": 100,
        "openemis_parent_bulk.xml": 100,
    }

    def _abs(self, rel):
        return os.path.join(BASE_DIR, rel)

    def test_bulk_files_exist(self):
        """All generated bulk demo files must be present on disk."""
        for rel in self.BULK_XML_FILES:
            self.assertTrue(
                os.path.isfile(self._abs(rel)),
                f"Missing bulk demo file: {rel}",
            )

    def test_bulk_files_valid_xml(self):
        """All bulk demo files must be well-formed XML."""
        for rel in self.BULK_XML_FILES:
            abs_path = self._abs(rel)
            if not os.path.isfile(abs_path):
                continue
            try:
                ET.parse(abs_path)
            except ET.ParseError as exc:
                self.fail(f"Invalid XML in {rel}: {exc}")

    def test_bulk_files_record_count(self):
        """Each bulk demo file must contain exactly 100 <record> elements."""
        for rel in self.BULK_XML_FILES:
            abs_path = self._abs(rel)
            if not os.path.isfile(abs_path):
                continue
            fname = os.path.basename(rel)
            expected = self.EXPECTED_COUNTS.get(fname, 100)
            tree = ET.parse(abs_path)
            records = tree.findall(".//record")
            self.assertEqual(
                len(records),
                expected,
                f"{rel}: expected {expected} records, found {len(records)}",
            )

    def test_classrooms_have_correct_model(self):
        """Classroom bulk file must reference 'op.classroom' model."""
        rel = "openeducat_classroom/demo/openemis_classrooms_bulk.xml"
        abs_path = self._abs(rel)
        if not os.path.isfile(abs_path):
            return
        tree = ET.parse(abs_path)
        for record in tree.findall(".//record"):
            model = record.get("model", "")
            self.assertEqual(
                model,
                "op.classroom",
                f"Unexpected model {model!r} in classroom bulk file",
            )

    def test_students_have_correct_model(self):
        """Student bulk file must reference 'op.student' model."""
        rel = "openeducat_core/demo/openemis_student_bulk.xml"
        abs_path = self._abs(rel)
        if not os.path.isfile(abs_path):
            return
        tree = ET.parse(abs_path)
        for record in tree.findall(".//record"):
            model = record.get("model", "")
            self.assertEqual(
                model,
                "op.student",
                f"Unexpected model {model!r} in student bulk file",
            )

    def test_faculty_have_correct_model(self):
        """Faculty bulk file must reference 'op.faculty' model."""
        rel = "openeducat_core/demo/openemis_faculty_bulk.xml"
        abs_path = self._abs(rel)
        if not os.path.isfile(abs_path):
            return
        tree = ET.parse(abs_path)
        for record in tree.findall(".//record"):
            model = record.get("model", "")
            self.assertEqual(
                model,
                "op.faculty",
                f"Unexpected model {model!r} in faculty bulk file",
            )

    def test_parents_have_correct_model(self):
        """Parent bulk file must reference 'op.parent' model."""
        rel = "openeducat_parent/demo/openemis_parent_bulk.xml"
        abs_path = self._abs(rel)
        if not os.path.isfile(abs_path):
            return
        tree = ET.parse(abs_path)
        for record in tree.findall(".//record"):
            model = record.get("model", "")
            self.assertEqual(
                model,
                "op.parent",
                f"Unexpected model {model!r} in parent bulk file",
            )


class TestOpenEMISFunctional(TransactionCase):
    """Functional smoke-tests – create & validate core openEMIS records."""

    def test_create_student(self):
        """Create a student record and verify field persistence."""
        partner = self.env['res.partner'].create({'name': 'Test Student openEMIS'})
        student = self.env['op.student'].create({
            'first_name': 'Test',
            'middle_name': 'O',
            'last_name': 'Student',
            'birth_date': '2005-06-15',
            'gender': 'f',
            'partner_id': partner.id,
        })
        self.assertEqual(student.first_name, 'Test')
        self.assertEqual(student.last_name, 'Student')
        self.assertTrue(student.active)

    def test_create_faculty(self):
        """Create a faculty record and verify field persistence."""
        partner = self.env['res.partner'].create({'name': 'Test Faculty openEMIS'})
        faculty = self.env['op.faculty'].create({
            'first_name': 'Faculty',
            'middle_name': 'E',
            'last_name': 'Member',
            'birth_date': '1980-03-22',
            'gender': 'male',
            'partner_id': partner.id,
        })
        self.assertEqual(faculty.first_name, 'Faculty')
        self.assertEqual(faculty.last_name, 'Member')
        self.assertTrue(faculty.active)

    def test_create_classroom(self):
        """Create a classroom record and verify it is searchable."""
        course = self.env['op.course'].search([], limit=1)
        classroom = self.env['op.classroom'].create({
            'code': 'TEST-CR-001',
            'name': 'openEMIS Test Classroom 001',
            'capacity': 35,
            'course_id': course.id,
        })
        self.assertEqual(classroom.code, 'TEST-CR-001')
        self.assertEqual(classroom.capacity, 35)
        found = self.env['op.classroom'].search([('code', '=', 'TEST-CR-001')])
        self.assertEqual(len(found), 1)

    def test_student_count_after_creation(self):
        """Bulk-create 10 students and verify search returns all of them."""
        partner_ids = []
        for idx in range(10):
            p = self.env['res.partner'].create(
                {'name': f'Bulk Student {idx:02d}'}
            )
            partner_ids.append(p.id)

        before = self.env['op.student'].search_count([])
        for idx, pid in enumerate(partner_ids):
            self.env['op.student'].create({
                'first_name': f'BulkS{idx:02d}',
                'last_name': 'OpenEMIS',
                'birth_date': '2003-01-01',
                'gender': 'm' if idx % 2 else 'f',
                'partner_id': pid,
            })
        after = self.env['op.student'].search_count([])
        self.assertEqual(after - before, 10, "Expected 10 new students")

    def test_faculty_count_after_creation(self):
        """Bulk-create 10 faculty members and verify search returns them."""
        before = self.env['op.faculty'].search_count([])
        for idx in range(10):
            p = self.env['res.partner'].create(
                {'name': f'Bulk Faculty {idx:02d}'}
            )
            self.env['op.faculty'].create({
                'first_name': f'BulkF{idx:02d}',
                'last_name': 'openEMIS',
                'birth_date': '1985-05-10',
                'gender': 'male' if idx % 2 else 'female',
                'partner_id': p.id,
            })
        after = self.env['op.faculty'].search_count([])
        self.assertEqual(after - before, 10, "Expected 10 new faculty members")

    def test_classroom_count_after_creation(self):
        """Bulk-create 10 classrooms and verify search returns them."""
        course = self.env['op.course'].search([], limit=1)
        before = self.env['op.classroom'].search_count([])
        for idx in range(10):
            self.env['op.classroom'].create({
                'code': f'BULK-{idx:03d}',
                'name': f'Bulk Classroom {idx:03d}',
                'capacity': 30,
                'course_id': course.id,
            })
        after = self.env['op.classroom'].search_count([])
        self.assertEqual(after - before, 10, "Expected 10 new classrooms")

    def test_student_course_enrollment(self):
        """Create a student-course enrollment and verify the relationship."""
        course = self.env['op.course'].search([], limit=1)
        batch = self.env['op.batch'].search(
            [('course_id', '=', course.id)], limit=1
        )
        partner = self.env['res.partner'].create({'name': 'Enrolled Student'})
        student = self.env['op.student'].create({
            'first_name': 'Enrolled',
            'last_name': 'Student',
            'birth_date': '2004-09-01',
            'gender': 'f',
            'partner_id': partner.id,
        })
        if batch:
            enrollment = self.env['op.student.course'].create({
                'student_id': student.id,
                'course_id': course.id,
                'batch_id': batch.id,
            })
            self.assertEqual(enrollment.student_id.id, student.id)
            self.assertEqual(enrollment.course_id.id, course.id)
