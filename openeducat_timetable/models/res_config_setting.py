from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_faculty_constraint = fields.Boolean(string="Faculty Constraint")
    is_classroom_constraint = fields.Boolean(string="Classroom Constraint")
    is_batch_and_subject_constraint = \
        fields.Boolean(string="Batch and Subject Constraint")
    is_batch_constraint = fields.Boolean(string="Batch Constraint")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            is_faculty_constraint=self.env['ir.config_parameter'].sudo().get_param(
                'timetable.is_faculty_constraint'),
            is_classroom_constraint=self.env['ir.config_parameter'].sudo().get_param(
                'timetable.is_classroom_constraint'),
            is_batch_and_subject_constraint=self.env['ir.config_parameter']
            .sudo().get_param(
                'timetable.is_batch_and_subject_constraint'),
            is_batch_constraint=self.env['ir.config_parameter']
            .sudo().get_param(
                'timetable.is_batch_constraint')
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        param = self.env['ir.config_parameter'].sudo()
        param.set_param('timetable.is_faculty_constraint', self.is_faculty_constraint)
        param.set_param('timetable.is_classroom_constraint',
                        self.is_classroom_constraint)
        param.set_param('timetable.is_batch_and_subject_constraint',
                        self.is_batch_and_subject_constraint)
        param.set_param('timetable.is_batch_constraint', self.is_batch_constraint)
