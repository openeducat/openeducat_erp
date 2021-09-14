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
from odoo.tests import common


class TestLibraryCommon(common.TransactionCase):
    def setUp(self):
        super(TestLibraryCommon, self).setUp()
        self.op_library_card_type = self.env['op.library.card.type']
        self.op_library_card = self.env['op.library.card']
        self.op_media = self.env['op.media']
        self.op_media_unit = self.env['op.media.unit']
        self.op_media_movement = self.env['op.media.movement']
        self.op_media_purchase = self.env['op.media.purchase']
        self.op_media_queue = self.env['op.media.queue']
        self.wizard_issue = self.env['issue.media']
        self.reserve_media = self.env['reserve.media']
        self.return_media = self.env['return.media']
