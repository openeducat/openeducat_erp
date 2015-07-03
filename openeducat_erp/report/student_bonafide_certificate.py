# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
##############################################################################

import time
from datetime import datetime
from openerp.report import report_sxw
from openerp.osv import osv, fields


class student_bonafide_certificate(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        super(student_bonafide_certificate, self).__init__(
            cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
        })
        self.context = context


class report_bonafide_certificate(osv.AbstractModel):
    _name = 'report.openeducat_erp.report_bonafide_certificate'
    _inherit = 'report.abstract_report'
    _template = 'openeducat_erp.report_bonafide_certificate'
    _wrapped_report_class = student_bonafide_certificate

#report_sxw.report_sxw('report.student.bonafide.certificate','op.student', 'addons/openeducat_erp/report/student_bonafide_certificate.rml', parser=student_bonafide_certificate, header='external')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
