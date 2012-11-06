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

class op_student(osv.osv):
    _name = 'op.student'
    _inherits = {'res.partner':'partner_id'}
    def _get_curr_roll_number(self, cr, uid, ids, fields, arg, context=None):
        ret_val = {}
        for self_obj in self.browse(cr, uid, ids, context=context):
            roll_no = 0
            seq = 0
            for roll_number in self_obj.roll_number_line:
                if roll_number.standard_id.sequence > seq:
                    roll_no = roll_number.roll_number
                    seq = roll_number.standard_id.sequence
            ret_val[self_obj.id] = roll_no

        return ret_val
    def _get_roll(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('op.roll.number').browse(cr, uid, ids, context=context):
            result[line.student_id.id] = True
        return result.keys()
    


    _columns = {
#            'name': fields.char(size=128, string='First Name', required=True),
            'middle_name': fields.char(size=128, string='Middle Name', required=True),
            'last_name': fields.char(size=128, string='Last Name', required=True),
            'birth_date': fields.date(string='Birth Date', required=True),
            'blood_group': fields.selection([('A+','A+ve'),('B+','B+ve'),('O+','O+ve'),('AB+','AB+ve'),('A-','A-ve'),('B-','B-ve'),('O-','O-ve'),('AB-','AB-ve')], string='Blood Group'),
            'gender': fields.selection([('m','Male'),('f','Female'),('o','Other')], string='Gender', required=True),
            'nationality': fields.many2one('res.country', string='Nationality'),
            'language': fields.many2one('res.lang', string='Language'),
            'category': fields.many2one('op.category', string='Category', required=True),
            'religion': fields.many2one('op.religion', string='Religion'),
            'library_card': fields.char(size=64, string='Library Card'),
            'emergency_contact': fields.many2one('res.partner', string='Emergency Contact'),
            'pan_card': fields.char(size=64, string='PAN Card'),
            'bank_acc_num': fields.char(size=64, string='Bank Acc Number'),
            'visa_info': fields.char(size=64, string='Visa Info'),
            'id_number': fields.char(size=64, string='ID Card Number'),
            'photo': fields.binary(string='Photo'),
            'course_id': fields.many2one('op.course', string='Course', required=True),
            'division_id': fields.many2one('op.division', string='Division'),
            'batch_id': fields.many2one('op.batch', string='Batch', required=True),
            'standard_id': fields.many2one('op.standard', string='Standard', required=True),
            'roll_number_line': fields.one2many('op.roll.number','student_id','Roll Number'),
            'partner_id': fields.many2one('res.partner', 'Partner',required=True, ondelete="cascade"),
            'roll_number': fields.function(_get_curr_roll_number,
                                method=True,
                                string='Current Roll Number',
                                type='char',
                                size=8,
                                store = {
                                    'op.roll.number': (_get_roll, [], 10),
                                }),
            'allocation_ids': fields.many2many('op.assignment', 'op_student_assignment_rel', 'op_student_id','op_assignment_id', string='Assignment'),
            'alumni_boolean': fields.boolean('Alumni Student'),
            'passing_year': fields.many2one('op.batch', string='Passing Year'),
            'current_position': fields.char(string='Current Position', size=256),
            'current_job': fields.char(string='Current Job', size=256),
            'email': fields.char(string='Email', size=128),
            'phone': fields.char(string='Phone Number', size=256),
            'user_id': fields.many2one('res.users', 'User'),
            'placement_line': fields.one2many('op.placement.offer', 'student_id', 'Placement Details'),
            'activity_log':fields.one2many('op.activity','student_id', 'Activity Log' ),
            'parent_ids': fields.many2many('op.parent', 'op_parent_student_rel', 'op_parent_id', 'op_student_id', string='Parent'),
    }


    def create_invoice(self, cr, uid, ids, context={}):
        """ Create invoice for fee payment process of student """

        invoice_pool = self.pool.get('account.invoice')

        default_fields = invoice_pool.fields_get(cr, uid, context=context)
        invoice_default = invoice_pool.default_get(cr, uid, default_fields, context=context)

        for student in self.browse(cr, uid, ids, context=context):

            onchange_partner = invoice_pool.onchange_partner_id(cr, uid, [], type='out_invoice',\
                                partner_id=student.partner_id.id)
            invoice_default.update(onchange_partner['value'])


            invoice_data = {
                            'partner_id': student.partner_id.id,
                            'date_invoice': time.strftime('%Y-%m-%d'),
                            'payment_term': student.standard_id and student.standard_id.id or student.course_id and student.course_id.id or False,
                            }

        invoice_default.update(invoice_data)
        invoice_id = invoice_pool.create(cr, uid, invoice_default, context=context)
        
        models_data = self.pool.get('ir.model.data')
        form_view = models_data.get_object_reference(cr, uid, 'account', 'invoice_form')
        tree_view = models_data.get_object_reference(cr, uid, 'account', 'invoice_tree')
        value = {
                'domain': str([('id', '=', invoice_id)]),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'account.invoice',
                'view_id': False,
                'views': [(form_view and form_view[1] or False, 'form'),
                          (tree_view and tree_view[1] or False, 'tree')],
                'type': 'ir.actions.act_window',
                'res_id': invoice_id,
                'target': 'current',
                'nodestroy': True
            }
        return value
op_student()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
