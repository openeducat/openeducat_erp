# -*- coding: utf-8 -*-
#/#############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2004-TODAY OpenEduCat Inc(<http://www.OpenEduCat Inc.com>).
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
from osv import osv, fields

class op_assignment_sub_history(osv.osv):
    _name = 'op.assignment.sub.history'

    _columns = {
            'assign_sub_id': fields.many2one('op.assignment.sub.line', string='Assignment'),
            'description': fields.text(string='Description'),
            'state': fields.selection([('d','Draft'),('s','Submitted'),('a','Accepted'),('r','Rejected'),('c','Change Req.')], string='State'),
            'change_date': fields.datetime(string='Submission Date'),
            'faculty_id': fields.many2one('op.faculty','Faculty'),
    }

op_assignment_sub_history()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
