# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
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
###############################################################################

import time

from openerp.osv import osv
from openerp.report import report_sxw


class StudentBonafideCertificate(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        super(StudentBonafideCertificate, self).__init__(
            cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
        })
        self.context = context


class ReportBonafideCertificate(osv.AbstractModel):
    _name = 'report.openeducat_erp.report_bonafide_certificate'
    _inherit = 'report.abstract_report'
    _template = 'openeducat_erp.report_bonafide_certificate'
    _wrapped_report_class = StudentBonafideCertificate

# report_sxw.report_sxw('report.student.bonafide.certificate','op.student',
#     'addons/openeducat_erp/report/student_bonafide_certificate.rml',
#     parser=student_bonafide_certificate, header='external')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
