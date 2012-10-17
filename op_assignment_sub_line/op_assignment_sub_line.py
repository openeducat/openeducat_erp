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
from osv import osv, fields
import time
from datetime import datetime, timedelta


class op_assignment_sub_line(osv.osv):
    _name = 'op.assignment.sub.line'
    
    _columns = {
            'assignment_id': fields.many2one('op.assignment', string='Assignment'),
            'student_id': fields.many2one('op.student', string='Student'),
            'description': fields.text(string='Description'),
            'state': fields.selection([('d','Draft'),('s','Submitted'),('a','Accepted'),('r','Rejected'),('c','Change Req.')], string='State'),
            'submission_date': fields.datetime(string='Submission Date', readonly=True),
            'note': fields.text(string='Note'),
            'history_line': fields.one2many('op.assignment.sub.history', 'assign_sub_id', string='Change History'),
    }
    
    _defaults = {
                 'submission_date': fields.date.context_today,
                 'state': 'd'
                 }
    
    def act_draft(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'d'})
        return True
    
    def act_submit(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'s'})
        return True
    
    def act_accept(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'a'})
        return True
    
    def act_change_req(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'c'})
        return True
    
    def act_reject(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'r'})
        return True
    
op_assignment_sub_line()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
