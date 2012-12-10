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

class op_health(osv.osv):
    _name = 'op.health'
    
    _description = """ Health Detail for Students and Faculties """
    
    _columns = {
            'partner_id': fields.many2one('res.partner', 'Student/Faculty', required=True),
            'height': fields.float('Height(C.M.)', required=True),
            'weight': fields.float('weight(K.G.)', required=True),
            'blood_group': fields.selection([('A+','A+ve'),('B+','B+ve'),('O+','O+ve'),\
                                             ('AB+','AB+ve'),('A-','A-ve'),('B-','B-ve'),\
                                             ('O-','O-ve'),('AB-','AB-ve')], string='Blood Group', required=True),
            'physical_challenges': fields.boolean('Physical Challenge?'),
            'physical_challenges_note': fields.text('Physical Challenge'),
            'major_diseases': fields.boolean('Major Diseases?'),
            'major_diseases_note': fields.text('Major Diseases'),
            'eyeglasses': fields.boolean('Eye Glasses?'),
            'eyeglasses_no': fields.char('Eye Glasses', size=64),
            'regular_checkup': fields.boolean('Any Regular Checkup Required?'),
            'health_line': fields.one2many('op.health.line', 'health_id', 'Checkup Line'),
    }

    _defaults = {
                'physical_challenges': False,
                'major_diseases': False,
                'regular_checkup': False,
                 }
    
##    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=100):
##        if not args:
##            args = []
##        ids = self.search(cr, user, [('serial', '=', name)]+ args, limit=limit, context=context)
##        ids += self.search(cr, user, [('name', operator, name)]+ args, limit=limit, context=context)
##        return self.name_get(cr, user, ids, context)
#
#    def name_get(self, cr, uid, ids, context={}):
#        result= []
#        if not all(ids):
#            return result
#        for health in self.browse(cr, uid, ids, context=context):
#            print "GGGGGGGGGG", health.student_id,health.faculty_id
#            name = health.faculty_id and health.faculty_id.name + ' ' + health.faculty_id.middle_name + ' ' + health.faculty_id.last_name or health.student_id and health.student_id.name + ' ' + health.student_id.middle_name + ' ' + health.student_id.last_name or False
#            result.append((pl.id,name))
#        return result
op_health()

class op_health_line(osv.osv):
    _name = 'op.health.line'
    
    _columns = {
            'health_id': fields.many2one('op.health', 'Health'),
            'date': fields.date('Date'),
            'name': fields.text('Checkup Detail', required=True),
            'recommendation': fields.text('Checkup Recommendation'),
    }

    _defaults = {
                'date': time.strftime('%Y-%m-%d'),
                 }

op_health_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
