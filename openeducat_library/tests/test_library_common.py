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
from odoo.tests import common
from odoo import fields


class TestLibraryCommon(common.TransactionCase):
    def setUp(self):
        super(TestLibraryCommon, self).setUp()
        # Modules
        self.op_author = self.env['op.author']
        self.op_publisher = self.env['op.publisher']
        self.op_media_type = self.env['op.media.type']
        self.op_media_tag = self.env['op.tag']
        self.op_media = self.env['op.media']
        self.op_media_unit = self.env['op.media.unit']
        self.op_library_card_type = self.env['op.library.card.type']
        self.op_library_card = self.env['op.library.card']
        self.op_media_movement = self.env['op.media.movement']
        self.op_media_purchase = self.env['op.media.purchase']
        self.op_media_queue = self.env['op.media.queue']
        self.wizard_issue = self.env['issue.media']
        self.reserve_media = self.env['reserve.media']
        self.return_media = self.env['return.media']

        # Setup base data
        self.partner = self.env['res.partner'].create({'name': 'Library User Partner'})
        self.student = self.env['op.student'].create({
            'partner_id': self.partner.id,
            'first_name': 'Lib',
            'last_name': 'Student',
            'gender': 'm',
            'birth_date': '2005-01-01',
        })
        self.author = self.op_author.search([('name', '=', 'Test Author')], limit=1) or \
                      self.op_author.create({'name': 'Test Author'})
        self.publisher = self.op_publisher.search([('name', '=', 'Test Publisher')], limit=1) or \
                         self.op_publisher.create({'name': 'Test Publisher'})
        self.media_type = self.op_media_type.search([('name', '=', 'Book')], limit=1) or \
                          self.op_media_type.create({'name': 'Book', 'code': 'B1'})
        self.media = self.op_media.search([('name', '=', 'Test Book')], limit=1) or \
                     self.op_media.create({
            'name': 'Test Book',
            'media_type_id': self.media_type.id,
            'isbn': '1234567890',
            'author_ids': [(6, 0, [self.author.id])],
            'publisher_ids': [(6, 0, [self.publisher.id])],
        })
        self.card_type = self.op_library_card_type.create({
            'name': 'Standard',
            'allow_media': 5,
            'duration': 14,
            'penalty_amt_per_day': 1.0,
        })
        self.library_card = self.op_library_card.create({
            'partner_id': self.partner.id,
            'library_card_type_id': self.card_type.id,
            'type': 'student',
            'student_id': self.student.id,
        })

        # Academic data for purchase requests
        self.course = self.env['op.course'].create({'name': 'Library Course', 'code': 'LC1'})
        self.subject = self.env['op.subject'].create({'name': 'Library Subject', 'code': 'LS1'})
