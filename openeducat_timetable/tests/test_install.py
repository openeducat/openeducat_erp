"""Tier A smoke tests for openeducat_timetable.

Assert the module installs cleanly, key models are registered, and
all shipped views parse without RelaxNG failures. Would have caught
the ``<group expand>`` RelaxNG rejection we hit earlier this session.
"""

from odoo.tests import common, tagged


@tagged('post_install', '-at_install')
class TestModuleInstall(common.TransactionCase):

    def test_module_installed(self):
        """openeducat_timetable is present in ir_module_module and marked
        installed."""
        module = self.env['ir.module.module'].search(
            [('name', '=', 'openeducat_timetable')], limit=1,
        )
        self.assertTrue(module, "Module record not found in ir_module_module")
        self.assertEqual(module.state, 'installed')

    def test_key_models_registered(self):
        """op.session (with our added student_ids field) is registered."""
        self.assertIn('op.session', self.env.registry)
        self.assertIn('student_ids', self.env['op.session']._fields)
        # Field must be M2M to op.student — regression: student_ids
        # briefly a M2O in an early draft.
        fld = self.env['op.session']._fields['student_ids']
        self.assertEqual(fld.type, 'many2many')
        self.assertEqual(fld.comodel_name, 'op.student')

    def test_start_datetime_is_indexed(self):
        """`start_datetime` has index=True after the perf-pass fix —
        without it, every portal / dashboard filter does a seq-scan.
        """
        fld = self.env['op.session']._fields['start_datetime']
        self.assertTrue(fld.index, "start_datetime should be indexed")

    def test_views_parse(self):
        """Every view arch shipped by this module parses through Odoo's
        RelaxNG validator. Would have caught our old
        ``<group expand>`` inside ``<search>`` regression.
        """
        views = self.env['ir.ui.view'].search([
            ('model', 'in', ['op.session']),
        ])
        # Force revalidation by touching arch; Odoo raises if invalid.
        for view in views:
            with self.subTest(view=view.xml_id or view.name):
                # `_check_xml` runs the full RNG pass
                view._check_xml()
