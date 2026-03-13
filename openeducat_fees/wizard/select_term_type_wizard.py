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


from odoo import fields, models


class SelectFeesTermTypeWizard(models.TransientModel):
    _name = "select.fees.term.type.wizard"
    _description = "Wizard For Fees Term Type"

    fees_terms = fields.Selection(
        selection=[('fixed_days', 'Fixed Fees of Days'),
                   ('fixed_date', 'Fixed Fees of Dates')], string='Fees Terms')

    def action_open_wizard(self):
        return {
            'name': 'Select Fees Term Type',
            'type': 'ir.actions.act_window',
            'res_model': 'select.fees.term.type.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('openeducat_fees.select_fees_term_type_form').id,
            'target': 'new',
        }

    def select_term_type(self):
        selected_term = self.fees_terms
        return {
            'name': 'name',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'op.fees.terms',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': {'default_fees_terms': selected_term},
        }
