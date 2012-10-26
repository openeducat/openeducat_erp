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
            'name': fields.char(size=128, string='First Name', required=True),
            'middle_name': fields.char(size=128, string='Middle Name', required=True),
            'last_name': fields.char(size=128, string='Last Name', required=True),
            'title': fields.many2one('res.partner.title','Title'),
            'application_number': fields.char(size=16, string='Application Number', required=True),
            'admission_date': fields.date(string='Admission Date', required=True),
            'application_date': fields.datetime(string='Application Date', required=True),
            'birth_date': fields.date(string='Birth Date', required=True),
            'course_id': fields.many2one('op.course', string='Course', required=True),
            'batch_id': fields.many2one('op.batch', string='Batch', required=True),
            'street': fields.char(size=256, string='Street'),
            'street2': fields.char(size=256, string='Street2'),
            'phone': fields.char(size=16, string='Phone'),
            'mobile': fields.char(size=16, string='Mobile'),
            'email': fields.char(size=256, string='Email'),
            'city': fields.char(size=64, string='City'),
            'zip': fields.char(size=8, string='Zip'),
            'state_id': fields.many2one('res.country.state', string='States'),
            'country_id': fields.many2one('res.country', string='Country'),
            'fees': fields.float(string='Fees'),
            'photo': fields.binary(string='Photo'),
            'state': fields.selection([('d','Draft'),('i','In Progress'),('s','Selected'),('r','Rejected'),('p','Pending'),('c','Cancel')],readonly=True,select=True, string='State'),
            'due_date': fields.date(string='Due Date'),
            'prev_institute': fields.char(size=256, string='Previous Institute'),
            'prev_course': fields.char(size=256, string='Previous Course'),
            'prev_result': fields.char(size=256, string='Previous Result'),
            'family_business': fields.char(size=256, string='Family Business'),
            'family_income': fields.float(string='Family Income'),
            'religion_id': fields.many2one('op.religion', string='Religion'),
            'category_id': fields.many2one('op.category', string='Category', required=True),
            'gender': fields.selection([('m','Male'),('f','Female'),('o','Other')], string='Gender', required=True),
            'standard_id': fields.many2one('op.standard', string='Standard', required=True),
            'division_id': fields.many2one('op.division', string='Division'),
    }

    _defaults = {
                 'application_number': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'op.admission'),
                 'state':'d',
    }

    _order = "application_number desc"



    def confirm_in_progress(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'i'})
        return True

    def confirm_selection(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'s'})
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

    def fee_paid(self, cr, uid, ids,context=None):
        if context is None:
            context = {}

        student_pool = self.pool.get('op.student')
        for field in self.browse(cr, uid, ids, context=context):
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

        models_data = self.pool.get('ir.model.data')
        form_view = models_data.get_object_reference(cr, uid, 'openeducat_erp', 'view_op_student_form')
        tree_view = models_data.get_object_reference(cr, uid, 'openeducat_erp', 'view_op_student_tree')
        value = {
                'domain': str([('id', '=', new_student)]),
                'view_type': 'form',
                'view_mode': 'tree, form',
                'res_model': 'op.student',
                'view_id': False,
                'views': [(form_view and form_view[1] or False, 'form'),
                          (tree_view and tree_view[1] or False, 'tree')],
                'type': 'ir.actions.act_window',
                'res_id': new_student,
                'target': 'current',
                'nodestroy': True
            }
        return value

op_admission()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
