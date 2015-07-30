# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from openerp import models, fields, api


class OpBookPurchase(models.Model):
    _name = 'op.book.purchase'

    name = fields.Char('Title', size=128, required=True)
    author_ids = fields.Char('Author', size=256)
    edition = fields.Text('Edition')
    publisher_ids = fields.Char('Publisher', size=256)
    course_ids = fields.Many2one('op.course', 'Course', required=True)
    subject_ids = fields.Many2one('op.subject', 'Subject', required=True)
    student_id = fields.Many2one(
        'op.student', 'Student',
        default=lambda self: self.env.user.user_line and
        self.env.user.user_line[0].id or False)
    faculty_id = fields.Many2one('op.faculty', 'Faculty')
    library_id = fields.Many2one('res.partner', 'Librarian')
    state = fields.Selection(
        [('d', 'Draft'), ('rq', 'Requested'), ('a', 'Accept'),
         ('r', 'Reject')], 'State', select=True, readonly=True, default='d')

    @api.one
    def act_draft(self):
        # Reminder:: Delete this method as it is not used.
        self.state = 'd'

    @api.one
    def act_requested(self):
        self.state = 'rq'

    @api.one
    def act_accept(self):
        self.state = 'a'

    @api.one
    def act_reject(self):
        self.state = 'r'

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
