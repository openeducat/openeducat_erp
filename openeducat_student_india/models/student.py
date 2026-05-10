from odoo import fields, models, api
from odoo.exceptions import ValidationError


class OpStudent(models.Model):
    _inherit = "op.student"

    country_id = fields.Many2one(
        'res.country',
        default=lambda self: self.env['res.country'].search([('code', '=', 'IN')], limit=1)
    )

    # India-specific fields
    aadhar_number = fields.Char(
        'Aadhar Number',
        size=12,
        help='12-digit unique Aadhar identification number'
    )
    religion = fields.Selection(
        [
            ('hindu', 'Hindu'),
            ('muslim', 'Muslim'),
            ('christian', 'Christian'),
            ('sikh', 'Sikh'),
            ('buddhist', 'Buddhist'),
            ('jain', 'Jain'),
            ('other', 'Other'),
        ],
        string='Religion'
    )
    caste = fields.Selection(
        [
            ('general', 'General'),
            ('sc', 'SC'),
            ('st', 'ST'),
            ('obc_ncl', 'OBC-NCL'),
            ('obc_cl', 'OBC-CL'),
        ],
        string='Caste'
    )

    _sql_constraints = [
        ('unique_aadhar_number',
         'unique(aadhar_number)',
         'Aadhar Number must be unique!')
    ]

    @api.constrains('aadhar_number')
    def _check_aadhar_format(self):
        """Validate Aadhar number format: must be 12 digits"""
        for record in self:
            if record.aadhar_number:
                # Remove any spaces
                aadhar = record.aadhar_number.replace(' ', '')

                # Check if it's exactly 12 digits
                if not aadhar.isdigit() or len(aadhar) != 12:
                    raise ValidationError(
                        'Aadhar Number must be exactly 12 digits'
                    )
