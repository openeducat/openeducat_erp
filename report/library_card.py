import time
from osv import osv
from report import report_sxw
import pooler

class op_library(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(op_library, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,

            })

report_sxw.report_sxw('report.op.library.report','op.student', 'addons/openeducat_erp/report/library_card.rml', parser=op_library, header=False)
