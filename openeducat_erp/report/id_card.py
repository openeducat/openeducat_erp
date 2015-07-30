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

from openerp import pooler
from openerp.addons.openeducat_erp import utils
from openerp.osv import osv
from openerp.report import report_sxw


class OpStudent(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        self.ctx = {}
        self.ctx = context.copy()
        super(OpStudent, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'render_image': self.render_image,
            'qr_data': self.qr_data,
            'get_obj': self.get_obj,
            'get_address': self.get_address,
        })

    def get_obj(self):
        student_list = []
        for student in pooler.get_pool(self.cr.dbname).get(
            self.ctx.get('active_model', False)).browse(
                self.cr, self.uid, self.ctx['active_ids']):
            student_list.append(student)
        return student_list

    def render_image(self, barcode):
        barcode = utils.get_barcode_image(value=barcode, code='QR')
        return barcode

    def get_address(self, student):
        addr = {
            'street': student.street or '',
            'street2': student.street2 or '',
            'city': student.city or '',
            'zip': student.zip or '',
            'phone': student.phone or '',
            'email': student.email or '',
        }
        return [addr]

    def qr_data(self, student):
        student_data = {}
        student_data = {
            'name': ' '.join([student.name,
                              student.middle_name,
                              student.last_name]),
            'roll_number': student.roll_number or '',
            'blood_group': student.blood_group or '',
            'course': student.course_id.name,
            'birth_date': student.birth_date or '',
            'address': '%s %s %s %s %s %s' % (student.street or '',
                                              student.street2 or '',
                                              student.city or '',
                                              student.zip or '',
                                              student.phone or '',
                                              student.email or '',
                                              )
        }
        qr = utils.get_barcode_image(value=student_data, code='QR')
        return qr


class ReportStudentIdcard(osv.AbstractModel):
    _name = 'report.openeducat_erp.report_student_idcard'
    _inherit = 'report.abstract_report'
    _template = 'openeducat_erp.report_student_idcard'
    _wrapped_report_class = OpStudent

# report_sxw.report_sxw('report.op.student.report','op.student',
#                       'addons/openeducat_erp/report/id_card.rml',
#                       parser=op_student, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
