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

class op_faculty(osv.osv):
    _name = 'op.faculty'
    _inherits = {'res.partner':'partner_id'}

    _columns = {
            'partner_id': fields.many2one('res.partner', 'Partner',required=True, ondelete="cascade"),
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
            'emergency_contact': fields.many2one('res.partner.address', string='Emergency Contact'),
            'pan_card': fields.char(size=64, string='PAN Card'),
            'bank_acc_num': fields.char(size=64, string='Bank Acc Number'),
            'visa_info': fields.char(size=64, string='Visa Info'),
            'id_number': fields.char(size=64, string='ID Card Number'),
            'photo': fields.binary(string='Photo'),
            'login': fields.related('user_id', 'login', type='char', string='Login', readonly=1),
            'last_login': fields.related('user_id', 'date', type='datetime', string='Latest Connection', readonly=1),
            'timetable_ids':fields.one2many('op.timetable','faculty_id','Time table'),
            'faculty_subject_ids': fields.many2many('op.subject', 'faculty_subject_rel', 'op_faculty_id', 'op_subject_id', string='Subjects'),
    }

op_faculty()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
