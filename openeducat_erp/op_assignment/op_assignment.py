# -*- coding: utf-8 -*-
#/#############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2004-TODAY Tech-Receptives(<http://www.tech-receptives.com>).
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
#/#############################################################################
from openerp.osv import osv, fields

class op_assignment(osv.osv):
    _name = 'op.assignment'

    _columns = {
            'name': fields.char(size=16, string='Name', required=True),
            'course_id': fields.many2one('op.course', string='Course', required=True),
            'standard_id': fields.many2one('op.standard', string='Standard', required=True),
            'division_id': fields.many2one('op.division', string='Division'),
            'subject_id': fields.many2one('op.subject', string='Subject', required=True),
            'faculty_id': fields.many2one('op.faculty', string='Faculty', required=True),
            'marks': fields.float(string='Marks'),
            'description': fields.text(string='Description', required=True),
            'type': fields.many2one('op.exam.type', string='Type', required=True),
            'state': fields.selection([('d','Draft'),('p','Publish'),('f','Finished')], string='State', required=True),
            'issued_date': fields.datetime(string='Issued Date', required=True),
            'submission_date': fields.datetime(string='Submission Date', required=True),
            'allocation_ids': fields.many2many('op.student', 'op_student_assignment_rel', 'op_assignment_id', 'op_student_id', string='Allocated To'),
            'assignment_sub_line': fields.one2many('op.assignment.sub.line', 'assignment_id', string='Submissions'),
            'reviewer': fields.many2one('op.faculty', 'Reviewer')
    }

    _defaults = {
                 'state':'d',
                 }

    def act_draft(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'d'})
        return True

    def act_publish(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'p'})
        return True

    def act_finish(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'f'})
        return True


op_assignment()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
