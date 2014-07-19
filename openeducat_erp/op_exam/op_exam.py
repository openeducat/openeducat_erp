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
from datetime import datetime

class op_exam_session(osv.osv):
    _name = 'op.exam.session'
    _description = 'Exam Session'

    _columns = {
            'name': fields.char(size=256, string='Exam', required=True),
            'course_id': fields.many2one('op.course', string='Course', required=True),
            'batch_id': fields.many2one('op.batch', string='Batch', required=True),
            'standard_id': fields.many2one('op.standard', string='Standard', required=True),
            'division_id': fields.many2one('op.division', string='Division'),
            'exam_code': fields.char(size=8, string='Exam Code', required=True),
            'start_time': fields.datetime(string='Start Time', required=True),
            'end_time': fields.datetime(string='End Time', required=True),
            'room_id': fields.many2one('op.exam.room', 'Room', required=True),
            'exam_ids':fields.one2many('op.exam','session_id','Exams'),

    }
    
    def _check_date_time(self, cr, uid, ids, context=None):
        for self_obj in self.browse(cr, uid, ids): 
            if self_obj.start_time > self_obj.end_time:
                return False
        return True
    
    _constraints = [
        (_check_date_time, 'Start Time Should be greater than End Time .', ['start_time','end_time']),
    ]
    
    def generate_result(self, cr, uid, ids, context={}):
        stu_pool = self.pool.get('op.student')
        for self_obj in self.browse(cr, uid, ids, context=context):
            for exam in self_obj.exam_ids:
                return True

op_exam_session()

class op_exam(osv.osv):
    _name = 'op.exam'

    def _get_total_marks(self, cr, uid, ids, field_name, arg, context={}):
        res = {}
        for self_obj in self.browse(cr, uid, ids, context=context):
            res[self_obj.id] = 0.00
            total_mark = 0.00
            if self_obj.exam_line:
                for line in self_obj.exam_line:
                    total_mark += line.total_marks
                res[self_obj.id] = total_mark
        
        return res
    
    def _get_total_passing_mark(self, cr, uid, ids, field_name, arg, context={}):
        res = {}
        for self_obj in self.browse(cr, uid, ids, context=context):
            res[self_obj.id] = 0.00
            total_pass = 0.00
            if self_obj.exam_line:
                for line in self_obj.exam_line:
                    total_pass += line.min_marks
                res[self_obj.id] = total_pass
        return res
    _columns = {
            'session_id':fields.many2one('op.exam.session','Exam Session'),
            'subject_id': fields.many2one('op.subject', string='Subject', required=True),
            'division_id': fields.many2one('op.division', string='Division'),
            'exam_code': fields.char(size=8, string='Exam Code', required=True),
            'exam_type': fields.many2one('op.exam.type', string='Exam Type', required=True),
            'evaluation_type': fields.selection([('normal','Normal'),('GPA','GPA'),('CWA','CWA'),('CCE','CCE')], string='Evaluation Type', required=True),
            'attendees_line': fields.one2many('op.exam.attendees', 'exam_id', string='Attendees', required=True),
            'venue': fields.many2one('res.partner', string='Venue'),
            'start_time': fields.datetime(string='Start Time', required=True),
            'end_time': fields.datetime(string='End Time', required=True),
            'state': fields.selection([('n','New Exam'),('h','Held'),('s','Scheduled'),('d','Done'),('c','Cancelled')], string='State', select=True, readonly=True),
            'note': fields.text(string='Note'),
            'responsible_id': fields.many2many('op.faculty', 'exam_faculty_rel', 'op_exam_id', 'op_faculty_id', string='Responsible'),
            'name': fields.char(size=256, string='Exam', required=True),
            'total_marks':fields.float('Total Marks'),
            'min_marks':fields.float('Passing Marks'),
    }

    _defaults = {
                 'state':'n'
    }
    
    def _check_date_time(self, cr, uid, ids, context=None):
        for self_obj in self.browse(cr, uid, ids): 
            if self_obj.start_time > self_obj.end_time:
                return False
        return True
    
    _constraints = [
        (_check_date_time, 'Start Time Should be greater than End Time .', ['start_time','end_time']),
    ]
    
    def act_held(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'h'})
        return True
    
    def act_done(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'d'})
        return True
    
    def act_schedule(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'s'})
        return True

    def act_cancel(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'c'})
        return True

    def act_new_exam(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'n'})
        return True

op_exam()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: