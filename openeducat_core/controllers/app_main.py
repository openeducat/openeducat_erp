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

from flectra import http
from flectra.http import request
from flectra.addons.portal.controllers.web import \
    Home as home


class OpeneducatHome(home):

    @http.route()
    def web_login(self, redirect=None, *args, **kw):
        response = super(OpeneducatHome, self).web_login(
            redirect=redirect, *args, **kw)
        if not redirect and request.params['login_success']:
            if request.env['res.users'].browse(request.uid).has_group(
                    'base.group_user'):
                redirect = b'/web?' + request.httprequest.query_string
            else:
                if request.env.user.is_parent:
                    redirect = '/my/child'
                else:
                    redirect = '/my/home'
            return http.redirect_with_hash(redirect)
        return response

    def _login_redirect(self, uid, redirect=None):
        if request.env.user.is_parent:
            return '/my/child'
        return '/my/home'
