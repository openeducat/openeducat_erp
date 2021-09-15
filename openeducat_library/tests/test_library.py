# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
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

from logging import info
import time
from .test_library_common import TestLibraryCommon


class TestMedia(TestLibraryCommon):

    def setUp(self):
        super(TestMedia, self).setUp()

    def test_case_media(self):
        media = self.op_media.search([])
        if not media:
            raise AssertionError(
                'Error in data, please check for library media details')
        info('  Details Of Library Media:.....')
        for record in media:
            info('      Name : %s' % record.name)
            info('      Media Type : %s' % record.media_type_id.name)
            info('      ISBN Code : %s' % record.isbn)
            info('      Course : %s' % record.course_ids.name)


class TestMediaUnit(TestLibraryCommon):

    def setUp(self):
        super(TestMediaUnit, self).setUp()

    def test_case_media_unit(self):
        mediaunit = self.op_media_unit.create({
            'name': 'Troposhere In Detail unit-006',
            'barcode': 'MUB0000067',
            'media_id': self.env.ref('openeducat_library.op_media_1').id,
        })
        mediaunit.name_search('mediaunit.name')


class TestMediaMovement(TestLibraryCommon):

    def setUp(self):
        super(TestMediaMovement, self).setUp()

    def test_case_media_movement(self):
        mediamovement = self.op_media_movement.search([])
        if not mediamovement:
            raise AssertionError(
                'Error in data, '
                'please check for library media movement details')
        info('  Details Of Library Media Movements:.....')
        for record in mediamovement:
            info('      Media : %s' % record.media_id.name)
            info('      Media Unit : %s' % record.media_unit_id.name)
            info('      Person : %s' % record.partner_id.name)
            info('      Library Card : %s' % record.library_card_id.number)
            record._check_date()
            record.check_actual_return_date()
            record.onchange_media_unit_id()
            record.onchange_library_card_id()
            record.onchange_issued_date()
            record.issue_media()


class TestMediaPurchase(TestLibraryCommon):

    def setUp(self):
        super(TestMediaPurchase, self).setUp()

    def test_case_media_purchase(self):
        mediapurchase = self.op_media_purchase.create({
            'name': 'Accounting Made Simple',
            'author': 'Mike Piper',
            'requested_id':
                self.env.ref('openeducat_core.op_res_partner_1').id,
            'course_ids': self.env.ref('openeducat_core.op_course_1').id,
            'subject_ids': self.env.ref('openeducat_core.op_subject_1').id
        })
        info('  Details Of Library Media Purchase:.....')
        for record in mediapurchase:
            info('      Title : %s' % record.name)
            info('      Author : %s' % record.author)
            info('      Requested By : %s' % record.requested_id.name)
            info('      Course : %s' % record.course_ids.name)
            info('      Subject : %s' % record.subject_ids.name)
            record.act_requested()
            record.act_accept()
            record.act_reject()


class TestMediaQueue(TestLibraryCommon):

    def setUp(self):
        super(TestMediaQueue, self).setUp()

    def test_case_media_queue(self):
        mediaqueue = self.op_media_queue.create({
            'name': 'QUE001',
            'media_id': self.env.ref('openeducat_library.op_media_1').id,
            'date_from':  time.strftime('%Y-%m-01'),
            'date_to':  time.strftime('%Y-%m-01'),
        })
        info('  Details Of Library Media Queue:.....')
        for record in mediaqueue:
            record.onchange_user()
            record._check_date()
            record.do_reject()
            record.do_accept()
            record.do_request_again()


class TestLibraryCardType(TestLibraryCommon):

    def setUp(self):
        super(TestLibraryCardType, self).setUp()

    def test_case_library_card_type(self):
        cardtype = self.op_library_card_type.search([])
        if not cardtype:
            raise AssertionError(
                'Error in data, please check for library card type details')
        info('  Details Of Library Card Type:.....')
        for record in cardtype:
            info('      Name : %s' % record.name)
            info('      No of medias Allowed : %s' % record.allow_media)
            info('      Duration : %s' % record.duration)
            info('      Penalty : %s' % record.penalty_amt_per_day)
            record.check_details()


class TestLibraryCard(TestLibraryCommon):

    def setUp(self):
        super(TestLibraryCard, self).setUp()

    def test_case_library_card(self):
        card = self.op_library_card.create({
            'partner_id': self.env.ref('openeducat_core.op_res_partner_1').id,
            'number': 'LCB0000000018',
            'library_card_type_id':
                self.env.ref('openeducat_library.op_library_card_type_1').id,
            'issue_date':  time.strftime('%Y-%m-01'),
            'type': 'student'
        })
        if not card:
            raise AssertionError(
                'Error in data, please check for library card details')
        info('  Details Of Library Card:.....')
        for record in card:
            info('      Number : %s' % record.number)
            info('      Card Type : %s' % record.library_card_type_id.name)
            info('      Student/Faculty : %s' % record.partner_id.name)
            info('      Issue Date : %s' % record.issue_date)
            record.onchange_type()
            record.onchange_student_faculty()


class TestWizardIssue(TestLibraryCommon):

    def setUp(self):
        super(TestWizardIssue, self).setUp()

    def test_case_wizard_issue(self):
        wizard = self.wizard_issue.create({
            'media_id': self.env.ref('openeducat_library.op_media_1').id,
            'media_unit_id':
                self.env.ref('openeducat_library.op_media_unit_3').id,
            'type': 'student',
            'library_card_id':
                self.env.ref('openeducat_library.op_library_card_type_1').id,
            'issued_date': time.strftime('%Y-%m-01'),
            'return_date':  time.strftime('%Y-%m-01')
        })
        wizard.do_issue()
        wizard._check_date()
        wizard.onchange_library_card_id()


class TestWizardReserve(TestLibraryCommon):

    def setUp(self):
        super(TestWizardReserve, self).setUp()

    def test_case_wizard_reserve(self):
        reserve = self.reserve_media.create({
            'partner_id': self.env.ref('openeducat_core.op_res_partner_1').id,
        })
        reserve.set_partner()


class TestWizardReturn(TestLibraryCommon):

    def setUp(self):
        super(TestWizardReturn, self).setUp()

    def test_case_wizard_return(self):
        return_wizard = self.return_media.create({
            'media_id': self.env.ref('openeducat_library.op_media_1').id,
            'media_unit_id':
                self.env.ref('openeducat_library.op_media_unit_2').id,
        })
        return_wizard.do_return()
