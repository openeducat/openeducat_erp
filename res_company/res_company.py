from osv import osv, fields

class res_company(osv.osv):
    _inherit = "res.company"
    _columns = {
                'signature': fields.binary('Signature'),
                }
res_company()