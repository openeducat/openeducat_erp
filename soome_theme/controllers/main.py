from odoo import http
from odoo.http import request, Response
import os

class SoomeTheme(http.Controller):

    @http.route('/web/binary/company_logo', type='http', auth='none')
    def company_logo(self, dbname=None, **kwargs):
        if not dbname:
            logo_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'static', 'src', 'img', 'soome_logo.png'
            )
            with open(logo_path, 'rb') as f:
                return Response(f.read(), content_type='image/png')
        return request.redirect(f'/web/binary/company_logo?dbname={dbname}')
