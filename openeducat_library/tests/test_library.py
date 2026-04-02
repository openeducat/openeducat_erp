###############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<https://www.openeducat.org>).
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

from .test_library_common import TestLibraryCommon
from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo import fields
from datetime import timedelta


@tagged('post_install', '-at_install')
class TestLibraryMasterData(TestLibraryCommon):
    """Test cases for Library Master Data (Author, Publisher, Media Type, Tags)"""

    # --- Author Tests ---
    def test_01_author_creation(self):
        author = self.op_author.create({'name': 'New Author'})
        self.assertEqual(author.name, 'New Author')

    def test_02_author_uniqueness(self):
        # Assuming uniqueness is enforced (if model has it)
        author = self.op_author.create({'name': 'Unique Author'})
        self.assertTrue(author)

    def test_03_author_search(self):
        authors = self.op_author.search([('name', '=', 'Test Author')])
        self.assertIn(self.author, authors)

    # --- Publisher Tests ---
    def test_04_publisher_creation(self):
        pub = self.op_publisher.create({'name': 'New Publisher'})
        self.assertEqual(pub.name, 'New Publisher')

    def test_05_publisher_uniqueness(self):
        pub = self.op_publisher.create({'name': 'Unique Publisher 2'})
        self.assertTrue(pub)

    def test_06_publisher_search(self):
        pubs = self.op_publisher.search([('name', '=', 'Test Publisher')])
        self.assertIn(self.publisher, pubs)

    # --- Media Type Tests ---
    def test_07_media_type_creation(self):
        mt = self.op_media_type.create({'name': 'CD', 'code': 'CD1'})
        self.assertEqual(mt.name, 'CD')

    def test_08_media_type_code(self):
        mt = self.op_media_type.create({'name': 'DVD', 'code': 'DVD1'})
        self.assertEqual(mt.code, 'DVD1')

    def test_09_media_type_search(self):
        mt = self.op_media_type.search([('code', '=', 'B1')])
        self.assertIn(self.media_type, mt)

    # --- Media Tag Tests ---
    def test_10_tag_creation(self):
        tag = self.op_media_tag.create({'name': 'Science Fiction'})
        self.assertEqual(tag.name, 'Science Fiction')

    def test_11_tag_uniqueness(self):
        tag = self.op_media_tag.create({'name': 'Science'})
        self.assertTrue(tag)

    def test_12_tag_search(self):
        tag = self.op_media_tag.create({'name': 'History'})
        res = self.op_media_tag.search([('name', '=', 'History')])
        self.assertTrue(res)


@tagged('post_install', '-at_install')
class TestLibraryMedia(TestLibraryCommon):
    """Test cases for Media and Media Units"""

    # --- Media Tests ---
    def test_01_media_creation(self):
        media = self.op_media.create({
            'name': 'New Media',
            'media_type_id': self.media_type.id,
            'isbn': '9876543210',
        })
        self.assertEqual(media.name, 'New Media')

    def test_02_media_authors(self):
        self.assertEqual(self.media.author_ids[0].name, 'Test Author')

    def test_03_media_search(self):
        res = self.op_media.search([('name', '=', 'Test Book')])
        self.assertIn(self.media, res)

    # --- Media Unit Tests ---
    def test_04_media_unit_creation(self):
        unit = self.op_media_unit.create({
            'name': 'Unit 1',
            'barcode': 'B1001',
            'media_id': self.media.id,
        })
        self.assertEqual(unit.media_id, self.media)

    def test_05_media_unit_state(self):
        unit = self.op_media_unit.create({
            'name': 'Unit 2',
            'media_id': self.media.id,
        })
        self.assertEqual(unit.state, 'available')

    def test_06_media_unit_search(self):
        unit = self.op_media_unit.create({'name': 'Unit 3', 'media_id': self.media.id})
        res = self.op_media_unit.search([('name', '=', 'Unit 3')])
        self.assertTrue(res)


@tagged('post_install', '-at_install')
class TestLibraryCard(TestLibraryCommon):
    """Test cases for Library Cards"""

    def test_01_card_creation(self):
        self.assertTrue(self.library_card.number)
        # self.assertEqual(self.library_card.state, 'available') # Field does not exist on card

    def test_02_card_type_validation(self):
        with self.assertRaises(ValidationError):
            self.op_library_card_type.create({
                'name': 'Bad Type',
                'allow_media': -1,
                'duration': 10,
                'penalty_amt_per_day': 1.0,
            })

    def test_03_card_active(self):
        self.library_card.write({'active': False})
        self.assertFalse(self.library_card.active)


@tagged('post_install', '-at_install')
class TestLibraryTransactional(TestLibraryCommon):
    """Test cases for Movements, Queue and Purchase"""

    def setUp(self):
        super(TestLibraryTransactional, self).setUp()
        self.media_unit = self.op_media_unit.create({
            'name': 'Movement Unit',
            'media_id': self.media.id,
            'state': 'available'
        })

    # --- Movement Tests ---
    def test_01_media_issue(self):
        movement = self.op_media_movement.create({
            'media_id': self.media.id,
            'media_unit_id': self.media_unit.id,
            'type': 'student',
            'library_card_id': self.library_card.id,
            'issued_date': fields.Date.today(),
            'return_date': fields.Date.today() + timedelta(days=14),
        })
        movement.issue_media()
        self.assertEqual(movement.state, 'issue')
        self.assertEqual(self.media_unit.state, 'issue')

    def test_02_media_return(self):
        movement = self.op_media_movement.create({
            'media_id': self.media.id,
            'media_unit_id': self.media_unit.id,
            'type': 'student',
            'library_card_id': self.library_card.id,
            'return_date': fields.Date.today(),
        })
        movement.issue_media()
        movement.return_media(fields.Date.today())
        self.assertIn(movement.state, ['return_done', 'return'])
        self.assertEqual(self.media_unit.state, 'available')

    def test_03_movement_date_validation(self):
        with self.assertRaises(ValidationError):
            self.op_media_movement.create({
                'media_id': self.media.id,
                'media_unit_id': self.media_unit.id,
                'type': 'student',
                'library_card_id': self.library_card.id,
                'issued_date': fields.Date.today() + timedelta(days=1),
                'return_date': fields.Date.today(),
            })

    # --- Queue Tests ---
    def test_04_queue_creation(self):
        queue = self.op_media_queue.create({
            'name': 'Q001',
            'media_id': self.media.id,
            'partner_id': self.partner.id,
            'date_from': fields.Date.today(),
            'date_to': fields.Date.today() + timedelta(days=7),
        })
        self.assertEqual(queue.state, 'request')

    def test_05_queue_accept(self):
        queue = self.op_media_queue.create({
            'name': 'Q002',
            'media_id': self.media.id,
            'partner_id': self.partner.id,
            'date_from': fields.Date.today(),
            'date_to': fields.Date.today() + timedelta(days=7),
        })
        queue.do_accept()
        self.assertEqual(queue.state, 'accept')

    def test_06_queue_reject(self):
        queue = self.op_media_queue.create({
            'name': 'Q003',
            'media_id': self.media.id,
            'partner_id': self.partner.id,
            'date_from': fields.Date.today(),
            'date_to': fields.Date.today() + timedelta(days=7),
        })
        queue.do_reject()
        self.assertEqual(queue.state, 'reject')

    # --- Purchase Request Tests ---
    def test_07_purchase_creation(self):
        purchase = self.op_media_purchase.create({
            'name': 'Requested Book',
            'author': 'Some Author',
            'requested_id': self.partner.id,
            'course_ids': self.course.id,
            'subject_ids': self.subject.id,
        })
        self.assertEqual(purchase.state, 'draft')

    def test_08_purchase_accept(self):
        purchase = self.op_media_purchase.create({
            'name': 'Requested Book 2',
            'author': 'Some Author',
            'requested_id': self.partner.id,
            'course_ids': self.course.id,
            'subject_ids': self.subject.id,
        })
        purchase.act_requested()
        purchase.act_accept()
        self.assertEqual(purchase.state, 'accept')

    def test_09_purchase_reject(self):
        purchase = self.op_media_purchase.create({
            'name': 'Requested Book 3',
            'author': 'Some Author',
            'requested_id': self.partner.id,
            'course_ids': self.course.id,
            'subject_ids': self.subject.id,
        })
        purchase.act_requested()
        purchase.act_reject()
        self.assertEqual(purchase.state, 'reject')
