# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
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

import datetime
import logging
from ast import literal_eval

import requests
from odoo.exceptions import UserError
from odoo.tools import misc, ustr
from odoo.tools.translate import _
from odoo.models import AbstractModel

from odoo import api, release

OEC_API_ENDPOINT = "https://srv.openeducat.org/publisher-warranty/"

_logger = logging.getLogger(__name__)


class PublisherWarrantyContract(AbstractModel):
    _inherit = "publisher_warranty.contract"

    @api.model
    def _get_message_logs(self):
        Users = self.env['res.users']
        IrParamSudo = self.env['ir.config_parameter'].sudo()
        dbuuid = IrParamSudo.get_param('database.uuid')
        db_create_date = IrParamSudo.get_param('database.create_date')
        limit_date = datetime.datetime.now()
        limit_date = limit_date - datetime.timedelta(15)
        limit_date_str = limit_date.strftime(
            misc.DEFAULT_SERVER_DATETIME_FORMAT)
        nbr_users = Users.search_count([('active', '=', True)])
        nbr_active_users = Users.search_count([
            ("login_date", ">=", limit_date_str),
            ('active', '=', True)])
        nbr_share_users = 0
        nbr_active_share_users = 0
        if "share" in Users._fields:
            nbr_share_users = Users.search_count(
                [("share", "=", True),
                 ('active', '=', True)])
            nbr_active_share_users = Users.search_count(
                [("share", "=", True),
                 ("login_date", ">=", limit_date_str),
                 ('active', '=', True)])
        user = self.env.user
        domain = [('application', '=', True),
                  ('state', 'in', ['installed', 'to upgrade', 'to remove'])]
        apps = self.env['ir.module.module'].sudo().search_read(domain,
                                                               ['name'])
        web_base_url = IrParamSudo.get_param('web.base.url')
        msg = {
            "dbuuid": dbuuid,
            "nbr_users": nbr_users,
            "nbr_active_users": nbr_active_users,
            "nbr_share_users": nbr_share_users,
            "nbr_active_share_users": nbr_active_share_users,
            "dbname": self._cr.dbname,
            "db_create_date": db_create_date,
            "version": release.version,
            "language": user.lang,
            "web_base_url": web_base_url,
            "apps": [app['name'] for app in apps],
        }
        if user.partner_id.company_id:
            company_id = user.partner_id.company_id
            msg.update(company_id.read(["name", "email", "phone"])[0])
        return msg

    @api.model
    def _get_system_logs(self):
        msg = self._get_message_logs()
        arguments = {'arg0': ustr(msg), "action": "update"}
        r = requests.post(OEC_API_ENDPOINT, data=arguments, timeout=30)
        r.raise_for_status()
        return literal_eval(r.text)

    def update_notification_openeducat(self, cron_mode=True):
        res = super(PublisherWarrantyContract, self).update_notification()
        try:
            try:
                self._get_system_logs()
            except Exception:
                if cron_mode:  # we don't want to see any stack trace in cron
                    return False
                _logger.debug(
                    "Exception while sending a get logs messages", exc_info=1)
                raise UserError(_(
                    "Error during communication with the  warranty server."))
        except Exception:
            if cron_mode:
                return False  # we don't want to see any stack trace in cron
            else:
                raise
        return res
