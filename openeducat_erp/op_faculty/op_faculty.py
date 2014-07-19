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

class op_faculty(osv.osv):
    _name = 'op.faculty'
    _inherits = {'res.partner':'partner_id'}
    
    def create_employee(self, cr, uid, ids, context=None):
        
        self_obj = self.browse(cr, uid,ids, context=None)
        emp_obj = self.pool.get('hr.employee')
        vals = {
                    'name' : self_obj[0].name + ' '+self_obj[0].middle_name +' '+ self_obj[0].last_name,
                    'nationality' : self_obj[0].country_id ,
                     'gender': self_obj[0].gender,
                    
                 }
        emp_id = emp_obj.create(cr,uid,vals,context=None)
        self.pool.get('op.faculty').write(cr,uid,ids,{'emp_id':emp_id})
        return True
        
    _columns = {
            'partner_id': fields.many2one('res.partner', 'Partner',required=True, ondelete="cascade"),
            'middle_name': fields.char(size=128, string='Middle Name', required=True),
            'last_name': fields.char(size=128, string='Last Name', required=True),
            'birth_date': fields.date(string='Birth Date', required=True),
            'blood_group': fields.selection([('A+','A+ve'),('B+','B+ve'),('O+','O+ve'),('AB+','AB+ve'),('A-','A-ve'),('B-','B-ve'),('O-','O-ve'),('AB-','AB-ve')], string='Blood Group'),
            'gender': fields.selection([('male', 'Male'), ('female', 'Female')], 'Gender',required=True),
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
            'login': fields.related('user_id', 'login', type='char', string='Login', readonly=1),
            'last_login': fields.related('user_id', 'date', type='datetime', string='Latest Connection', readonly=1),
            'timetable_ids':fields.one2many('op.timetable','faculty_id','Time table'),
            'health_faculty_lines': fields.one2many('op.health', 'faculty_id', 'Health Detail'),
            'faculty_subject_ids': fields.many2many('op.subject', 'faculty_subject_rel', 'op_faculty_id', 'op_subject_id', string='Subjects'),
            'emp_id': fields.many2one('hr.employee', string='Employee'),
            
            
    }

op_faculty()

class hr_employee(osv.osv):
    
    _inherit = "hr.employee"
    
    def onchange_user(self, cr, uid, ids, user_id, context=None):
        work_email = False; address = False; emp_id = False
        number = False
        if user_id:
            user = self.pool.get('res.users').browse(cr, uid, user_id)
            user.partner_id.write({'supplier': True})
            address = user.partner_id.id
            work_email = user.email
            return {'value': {'work_email' : work_email, 'address_home_id': address, 'identification_id': number}, 'domain': {'address_id': [('id', '=', address)]}}
        return {}
    
    def onchange_address_id(self, cr, uid, ids, address,address_home, context=None):
        if address:
            address = self.pool.get('res.partner').browse(cr, uid, address, context=context)
            return {'value': {'work_phone': address.phone, 'mobile_phone': address.mobile}}
        if address_home and address:
            if address_home != address:
                raise osv.except_osv(_('Configuration Error!'), _('Home Address and working address should be same!'))
        return {'value': {}}

    def onchange_address_home_id(self, cr, uid, ids, address_home_id,address, context=None):
        emp_id = False
        if address_home_id and address:
            if address_home_id != address:
                raise osv.except_osv(_('Configuration Error!'), _('Home Address and working address should be same!'))
        if address_home_id:
            partner = self.pool.get('res.partner').browse(cr, uid, address_home_id)
            partner.write({'supplier': True, 'employee': True})            
        return {'value': {}}
    
    def onchange_company(self, cr, uid, ids, company, context=None):
        address_id = False
        if company:
            company_id = self.pool.get('res.company').browse(cr, uid, company, context=context)
            address = self.pool.get('res.partner').address_get(cr, uid, [company_id.partner_id.id], ['default'])
            address_id = address and address['default'] or False
        return {'value': {'address_id' : False}}



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
