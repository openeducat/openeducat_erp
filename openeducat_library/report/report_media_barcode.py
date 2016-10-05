# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import base64
from reportlab.graphics.barcode import createBarcodeDrawing
import time
from openerp import models, _
from openerp.exceptions import ValidationError
from openerp.report import report_sxw


class MediaBarcodeParser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        super(MediaBarcodeParser, self).__init__(
            cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_barcode': self.get_barcode,
        })

    def get_barcode(self, type, value, width=350, height=60, hr=1):
        """ genrating image for barcode """
        options = {}
        if width:
            options['width'] = width
        if height:
            options['height'] = height
        if hr:
            options['humanReadable'] = hr
        try:
            ret_val = createBarcodeDrawing(
                type, value=str(value), **options)
        except Exception, e:
            raise ValidationError(_('Error in barcode generation', e))
        image_data = ret_val.asString('png')
        return base64.encodestring(image_data)


class ReportMediaBarcode(models.AbstractModel):
    _name = 'report.openeducat_library.report_media_barcode'
    _inherit = 'report.abstract_report'
    _template = 'openeducat_library.report_media_barcode'
    _wrapped_report_class = MediaBarcodeParser
