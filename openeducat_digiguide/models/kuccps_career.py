###############################################################################
#
#    openEMIS
#    Copyright (C) 2009-TODAY openEMIS(<https://www.openemis.org>).
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

import json
import logging

import requests

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

KUCCPS_SYNC_STATUS = [
    ('pending', 'Pending'),
    ('synced', 'Synced'),
    ('error', 'Error'),
]


class OpKuccpsCareer(models.Model):
    """Represents a career / degree programme sourced from the Kenya
    Universities and Colleges Central Placement Service (KUCCPS).

    Records can be created manually or fetched automatically via the
    KUCCPS REST API using *action_sync_from_kuccps*."""

    _name = 'op.kuccps.career'
    _description = 'KUCCPS Career / Programme'
    _inherit = ['mail.thread']
    _order = 'name'

    name = fields.Char('Programme Name', required=True, tracking=True)
    kuccps_code = fields.Char('KUCCPS Code', index=True)
    cluster = fields.Char('Cluster / Cluster Weight')
    minimum_grade = fields.Char(
        'Minimum Grade',
        help="Minimum overall grade required (e.g. C+, B, A-)")
    minimum_points = fields.Float(
        'Minimum Points',
        help="Minimum KCSE cluster points required")
    required_subjects = fields.Text(
        'Required Subjects',
        help="Comma-separated subject requirements, e.g. "
             "Mathematics, Biology, Chemistry")
    institution_name = fields.Char('Institution')
    institution_type = fields.Selection([
        ('university', 'University'),
        ('college', 'College / TVET'),
    ], string='Institution Type')
    duration_years = fields.Float('Duration (Years)')
    description = fields.Text('Description')
    sync_status = fields.Selection(
        KUCCPS_SYNC_STATUS, string='Sync Status',
        default='pending', tracking=True)
    last_sync_date = fields.Datetime('Last Synced')
    raw_api_response = fields.Text(
        'Raw API Response', help="JSON response from the KUCCPS API")
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('unique_kuccps_code',
         'unique(kuccps_code)',
         'A career with this KUCCPS code already exists!'),
    ]

    # ------------------------------------------------------------------
    # KUCCPS API integration
    # ------------------------------------------------------------------

    @api.model
    def _get_kuccps_api_url(self):
        """Return the KUCCPS API base URL from system parameters."""
        return self.env['ir.config_parameter'].sudo().get_param(
            'digiguide.kuccps_api_url',
            default='https://api.kuccps.net/v1')

    @api.model
    def _get_kuccps_api_key(self):
        """Return the KUCCPS API key from system parameters."""
        return self.env['ir.config_parameter'].sudo().get_param(
            'digiguide.kuccps_api_key',
            default='')

    def _build_headers(self):
        api_key = self._get_kuccps_api_key()
        headers = {'Content-Type': 'application/json'}
        if api_key:
            headers['Authorization'] = 'Bearer %s' % api_key
        return headers

    @api.model
    def action_sync_from_kuccps(self):
        """Fetch career/programme data from the KUCCPS API and upsert records.

        The method expects the KUCCPS API to return JSON in the form:
        {
            "programmes": [
                {
                    "code": "...",
                    "name": "...",
                    "cluster": "...",
                    "minimum_grade": "...",
                    "minimum_points": ...,
                    "required_subjects": "...",
                    "institution": "...",
                    "institution_type": "university|college",
                    "duration_years": ...,
                    "description": "..."
                },
                ...
            ]
        }
        """
        base_url = self._get_kuccps_api_url()
        endpoint = '%s/programmes' % base_url.rstrip('/')
        headers = self._build_headers()

        try:
            response = requests.get(
                endpoint, headers=headers, timeout=30)
            response.raise_for_status()
        except requests.exceptions.ConnectionError as exc:
            raise UserError(
                _("Could not connect to the KUCCPS API: %s") % str(exc)
            ) from exc
        except requests.exceptions.Timeout as exc:
            raise UserError(
                _("The KUCCPS API request timed out: %s") % str(exc)
            ) from exc
        except requests.exceptions.HTTPError as exc:
            raise UserError(
                _("KUCCPS API returned an error (%s): %s")
                % (response.status_code, response.text)
            ) from exc

        try:
            data = response.json()
        except ValueError as exc:
            raise UserError(
                _("Invalid JSON received from KUCCPS API: %s") % str(exc)
            ) from exc

        programmes = data.get('programmes', [])
        created = updated = 0
        now = fields.Datetime.now()

        for prog in programmes:
            code = prog.get('code', '').strip()
            vals = {
                'name': prog.get('name', ''),
                'kuccps_code': code,
                'cluster': prog.get('cluster', ''),
                'minimum_grade': prog.get('minimum_grade', ''),
                'minimum_points': prog.get('minimum_points', 0.0),
                'required_subjects': prog.get('required_subjects', ''),
                'institution_name': prog.get('institution', ''),
                'institution_type': prog.get('institution_type', 'university'),
                'duration_years': prog.get('duration_years', 0.0),
                'description': prog.get('description', ''),
                'sync_status': 'synced',
                'last_sync_date': now,
                'raw_api_response': json.dumps(prog),
            }
            existing = self.search([('kuccps_code', '=', code)], limit=1)
            if existing:
                existing.write(vals)
                updated += 1
            else:
                self.create(vals)
                created += 1

        _logger.info(
            'KUCCPS sync complete: %d created, %d updated.', created, updated)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('KUCCPS Sync Complete'),
                'message': _(
                    '%d programmes created, %d updated.') % (created, updated),
                'type': 'success',
                'sticky': False,
            },
        }
