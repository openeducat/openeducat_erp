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
import pooler
import time
import netsvc

class op_admission(osv.osv):
    _name = 'op.admission'
    _rec_name = 'application_number'

    def copy(self, cr, uid, id, default=None, context=None):
        if not default:
            default = {}
        default.update({
            'state': 'd',
            'application_number': self.pool.get('ir.sequence').get(cr, uid, 'op.admission'),
        })
        return super(op_admission, self).copy(cr, uid, id, default, context=context)

    _columns = {
            'name': fields.char(size=128, string='First Name', required=True, states={'done':[('readonly',True)]}),
            'middle_name': fields.char(size=128, string='Middle Name', required=True, states={'done':[('readonly',True)]}),
            'last_name': fields.char(size=128, string='Last Name', required=True, states={'done': [('readonly', True)]}),
            'title': fields.many2one('res.partner.title','Title', states={'done': [('readonly', True)]}),
            'application_number': fields.char(size=16, string='Application Number', required=True, states={'done': [('readonly', True)]}),
            'admission_date': fields.date(string='Admission Date', required=True, states={'done': [('readonly', True)]}),
            'application_date': fields.datetime(string='Application Date', required=True, states={'done': [('readonly', True)]}),
            'birth_date': fields.date(string='Birth Date', required=True, states={'done': [('readonly', True)]}),
            'course_id': fields.many2one('op.course', string='Course', required=True, states={'done': [('readonly', True)]}),
            'batch_id': fields.many2one('op.batch', string='Batch', required=True, states={'done': [('readonly', True)]}),
            'street': fields.char(size=256, string='Street', states={'done': [('readonly', True)]}),
            'street2': fields.char(size=256, string='Street2', states={'done': [('readonly', True)]}),
            'phone': fields.char(size=16, string='Phone', states={'done': [('readonly', True)]}),
            'mobile': fields.char(size=16, string='Mobile', states={'done': [('readonly', True)]}),
            'email': fields.char(size=256, string='Email', states={'done': [('readonly', True)]}),
            'city': fields.char(size=64, string='City', states={'done': [('readonly', True)]}),
            'zip': fields.char(size=8, string='Zip', states={'done': [('readonly', True)]}),
            'state_id': fields.many2one('res.country.state', string='States', states={'done': [('readonly', True)]}),
            'country_id': fields.many2one('res.country', string='Country', states={'done': [('readonly', True)]}),
            'fees': fields.float(string='Fees', states={'done': [('readonly', True)]}),
            'photo': fields.binary(string='Photo', states={'done': [('readonly', True)]}),
            'state': fields.selection([('d','Draft'),('i','Confirm'),('s','Enroll'), ('done','Done') ,('r','Rejected'),('p','Pending'),('c','Cancel')],readonly=True,select=True, string='State'),
            'due_date': fields.date(string='Due Date', states={'done': [('readonly', True)]}),
            'prev_institute': fields.char(size=256, string='Previous Institute', states={'done': [('readonly', True)]}),
            'prev_course': fields.char(size=256, string='Previous Course', states={'done': [('readonly', True)]}),
            'prev_result': fields.char(size=256, string='Previous Result', states={'done': [('readonly', True)]}),
            'family_business': fields.char(size=256, string='Family Business', states={'done': [('readonly', True)]}),
            'family_income': fields.float(string='Family Income', states={'done': [('readonly', True)]}),
            'religion_id': fields.many2one('op.religion', string='Religion', states={'done': [('readonly', True)]}),
            'category_id': fields.many2one('op.category', string='Category', required=True, states={'done': [('readonly', True)]}),
            'gender': fields.selection([('m','Male'),('f','Female'),('o','Other')], string='Gender', required=True, states={'done': [('readonly', True)]}),
            'standard_id': fields.many2one('op.standard', string='Standard', required=True, states={'done': [('readonly', True)]}),
            'division_id': fields.many2one('op.division', string='Division', states={'done': [('readonly', True)]}),
            'student_id': fields.many2one('op.student', string='Student', states={'done': [('readonly', True)]}),
            'nbr': fields.integer('# of Admission', readonly=True),
            'gr_no': fields.boolean('Old Student??'),
            'gr_no_old': fields.char(string="GR Number old", size=10),
            'gr_no_new': fields.char(string="GR Number new", size=10),
            
    }

    _defaults = {
                 'application_number': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'op.admission'),
                 'state':'d',
                 'admission_date': time.strftime('%Y-%m-%d'),
                 'application_date': time.strftime('%Y-%m-%d %H:%M:%S'),
    }

    _order = "application_number desc"



    def confirm_in_progress(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'i'})
        return True

    def confirm_selection(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        student_pool = self.pool.get('op.student')
        for field in self.browse(cr, uid, ids, context=context):
            if field.gr_no == True:
                gr = field.gr_no_old
            else:
                gr = field.gr_no_new
            print 'GGGGGGGGGGG___________',gr
            vals = {
                    'title': field.title and field.title.id or False,
                    'name': field.name,
                    'middle_name': field.middle_name,
                    'last_name': field.last_name,
                    'birth_date':field.birth_date,
                    'gender': field.gender,
                    'category': field.category_id and field.category_id.id or False,
                    'course_id': field.course_id and field.course_id.id or False,
                    'batch_id': field.batch_id and field.batch_id.id or False,
                    'standard_id': field.standard_id and field.standard_id.id or False,
                    'religion': field.religion_id and field.religion_id.id or False,
                    'photo': field.photo or False,
                    'gr': gr,
                    'address':[(0,0,{
                                     'name': field.name or False,
                                     'type': 'invoice',
                                     'title': field.title and field.title.id or False,
                                     'street': field.street or False,
                                     'street2': field.street2 or False,
                                     'phone': field.phone or False,
                                     'mobile': field.mobile or False,
                                     'zip': field.zip or False,
                                     'city': field.city or False,
                                     'country_id': field.country_id and field.country_id.id or False,
                                     'state_id': field.state_id and field.state_id.id or False,
                                     })]
                    }
        new_student = student_pool.create(cr, uid, vals, context=context)
        self.write(cr,uid,ids,{'state':'s', 'student_id': new_student, 'nbr': 1})
        return True

    def confirm_rejected(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'r'})
        return True

    def confirm_pending(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'p'})
        return True

    def confirm_to_draft(self, cr, uid, ids, context=None):
        wf_service = netsvc.LocalService("workflow")
        self.write(cr,uid,ids,{'state':'d'})
        for inv_id in ids:
            wf_service.trg_delete(uid, 'op.admission', inv_id, cr)
            wf_service.trg_create(uid, 'op.admission', inv_id, cr)
        return True

    def confirm_cancel(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'c'})
        return True

    def open_student(self, cr, uid, ids,context={}):

        this_obj = self.browse(cr, uid, ids[0], context)
        student = self.pool.get('op.student').browse(cr, uid, this_obj.student_id.id, context)
        models_data = self.pool.get('ir.model.data')
        form_view = models_data.get_object_reference(cr, uid, 'openeducat_erp', 'view_op_student_form')
        tree_view = models_data.get_object_reference(cr, uid, 'openeducat_erp', 'view_op_student_tree')
        value = {
                'domain': str([('id', '=', student.id)]),
                'view_type': 'form',
                'view_mode': 'tree, form',
                'res_model': 'op.student',
                'view_id': False,
                'views': [(form_view and form_view[1] or False, 'form'),
                          (tree_view and tree_view[1] or False, 'tree')],
                'type': 'ir.actions.act_window',
                'res_id': student.id,
                'target': 'current',
                'nodestroy': True
            }
        self.write(cr,uid,ids,{'state':'done'})
        return value

op_admission()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
