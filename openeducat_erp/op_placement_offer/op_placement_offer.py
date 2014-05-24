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

from openerp.osv import osv,fields

class op_placement_offer(osv.osv):
    _name = 'op.placement.offer'
    _description = 'Placement Offer'

    _columns = {
                'name': fields.char('Company Name', required=True),
                'student_id': fields.many2one('op.student', 'Student Name', required=True),
                'join_date': fields.date(string='Join Date'),
                'offer_package': fields.char(string='Offered Package', size=256),
                'training_period': fields.char(string='Training Period', size=256),
                'state': fields.selection([('d','Draft'),('o','Offer'),('j','Join'),('r','Rejected'),('c','Cancel')], string='State')
    }
    
    _defaults = {
                 'state':'d',
    }
    
    def placement_offer(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'o'})
        return True

    def placement_join(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'j'})
        return True

    def confirm_rejected(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'r'})
        return True

    def confirm_to_draft(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'d'})
        return True

    def confirm_cancel(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'c'})
        return True

op_placement_offer()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
