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
from openerp.osv import osv
from openerp.report import report_sxw


class BookBarcodeParser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        self.ids_to_print = []
        self.ids_to_print = context.get('active_ids', False)
        self.model_name = context.get('active_model', False)
        super(BookBarcodeParser, self).__init__(
            cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'render_image': self.render_image,
        })

    def render_image(self):
        render_list = []
        for data in self.ids_to_print:
            book_obj = pooler.get_pool(self.cr.dbname).get(
                self.model_name).browse(self.cr, self.uid, data)
            render_data = {
                'name': book_obj.name,
                'book': book_obj.id_book
            }
            render_list.append(render_data)
        return render_list


class ReportBookBarcode(osv.AbstractModel):
    _name = 'report.openeducat_erp.report_book_barcode'
    _inherit = 'report.abstract_report'
    _template = 'openeducat_erp.report_book_barcode'
    _wrapped_report_class = BookBarcodeParser


# report_sxw.report_sxw('report.op.book.barcode', 'op.book',
#            'addons/openeducat_erp/report/book_barcode.rml',
#                      parser=book_barcode, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
