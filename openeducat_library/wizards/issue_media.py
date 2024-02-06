# -*- coding: utf-8 -*-
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

from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

from ..models import media_unit


class IssueMedia(models.TransientModel):
    """ Issue Media """
    _name = "issue.media"
    _description = "Issue Media Wizard"

    media_id = fields.Many2one('op.media', 'Media', required=True)
    media_unit_id = fields.Many2one('op.media.unit', 'Media Unit',
                                    required=True)
    type = fields.Selection(
        [('student', 'Student'), ('faculty', 'Faculty')],
        'Type', default='student', required=True)
    student_id = fields.Many2one('op.student', 'Student')
    faculty_id = fields.Many2one('op.faculty', 'Faculty')
    library_card_id = fields.Many2one(
        'op.library.card', 'Library Card', required=True)
    issued_date = fields.Date(
        'Issued Date', required=True, default=fields.Date.today())
    return_date = fields.Date('Return Date', required=True)

    @api.constrains('issued_date', 'return_date')
    def _check_date(self):
        if self.issued_date > self.return_date:
            raise ValidationError(_(
                'Return Date cannot be set before Issued Date.'))

    @api.onchange('library_card_id')
    def onchange_library_card_id(self):
        self.type = self.library_card_id.type
        self.student_id = self.library_card_id.student_id.id
        self.faculty_id = self.library_card_id.faculty_id.id
        self.return_date = datetime.today() + relativedelta(
            days=self.library_card_id.library_card_type_id.duration)

    def check_max_issue(self, student_id, library_card_id):
        media_movement_search = self.env["op.media.movement"].search(
            [('library_card_id', '=', library_card_id),
             ('student_id', '=', student_id),
             ('state', '=', 'issue')])
        if len(media_movement_search) < self.env["op.library.card"].browse(
                library_card_id).library_card_type_id.allow_media:
            return True
        else:
            return False

    def do_issue(self):
        for media in self:
            value = {}
            if media.check_max_issue(media.student_id.id,
                                     media.library_card_id.id):
                if media.media_unit_id.state and \
                        media.media_unit_id.state == 'available':
                    media_movement_create = {
                        'media_id': media.media_id.id,
                        'media_unit_id': media.media_unit_id.id,
                        'type': media.type,
                        'student_id': media.student_id.id or False,
                        'faculty_id': media.faculty_id.id or False,
                        'library_card_id': media.library_card_id.id,
                        'issued_date': media.issued_date,
                        'return_date': media.return_date,
                        'state': 'issue',
                    }
                    self.env['op.media.movement'].create(media_movement_create)
                    media.media_unit_id.state = 'issue'
                    value = {'type': 'ir.actions.act_window_close'}
                else:
                    raise UserError(_("media Unit can not be issued \
                    because it's state is : %s") % (dict(
                        media_unit.unit_states).get(
                        media.media_unit_id.state)))
            else:
                raise UserError(
                    _('Maximum Number of media allowed for %s is : %s') %
                    (media.student_id.name,
                     media.library_card_id.library_card_type_id.allow_media))
            return value
