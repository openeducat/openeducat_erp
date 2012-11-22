import time
from osv import osv
from report import report_sxw
import pooler

class op_transportation_detail(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(op_transportation_detail, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,

            })

report_sxw.report_sxw('report.op.transport.detail.report',
                      'op.transportation', 'addons/openeducat_erp/report/transport_detail.rml', 
                      parser=op_transportation_detail, header='external')
