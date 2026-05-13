from odoo import api, models


class BonafideCertificateReport(models.AbstractModel):
    _name = 'report.openeducat_core.report_student_bonafide'
    _description = 'Bonafide Certificate Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env.context.get('active_model')
        if not model:
            report_name = 'openeducat_core.report_student_bonafide'
            report = self.env['ir.actions.report']._get_report_from_name(report_name)
            model = report.model

        active_ids = self.env.context.get('active_ids') or docids
        docs = self.env[model].browse(active_ids)

        for student in docs:
            if not student.certificate_number:
                student.certificate_number = (
                    self.env['ir.sequence'].next_by_code('op.student.certificate')
                )

        return {
            'doc_ids': docids,
            'doc_model': model,
            'docs': docs,
            'data': data or {},
        }
