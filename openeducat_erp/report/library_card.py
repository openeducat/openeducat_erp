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

import time
from openerp.osv import osv
from openerp.report import report_sxw
from openerp import pooler

class op_library(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(op_library, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,

            })

report_sxw.report_sxw('report.op.library.report','op.student', 'addons/openeducat_erp/report/library_card.rml', parser=op_library, header=False)
