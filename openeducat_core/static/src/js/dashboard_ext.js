odoo.define('openeducat_core.dashboard_ext', function(require) {
    "use strict";
    var Widget = require('web.Widget');
    var Dashboard = require('web_settings_dashboard');
    Dashboard.Dashboard.include({
        init: function(parent, data) {
            this._super.apply(this, arguments);
            this.all_dashboards = ['apps', 'invitations', 'company', 'share', 'orgInfo'];
        },
        load_orgInfo: function(data) {
            return new DashboardOrgInfo(this, data.orgInfo).replace(this.$('.o_dashboard_org_info'));
        },
    });
    var DashboardOrgInfo = Widget.extend({
        template: 'DashboardOrgInfo',
        init: function(parent, data) {
            this.data = data;
            this.parent = parent;
            return this._super.apply(this, arguments);
        },
        start: function() {
            var self = this;
            this._super.apply(this, arguments);
            setTimeout(function() {
                self._rpc({
                    model: 'ir.config_parameter',
                    method: 'get_param',
                    args: ['database.uuid'],
                }).then(function(dbuuid) {
                        var apps = $('.org_logo_with_uuid_name').attr('data-app-name');
                        var src = 'https://srv.openeducat.org/get-org-logo';
                        $('.org_logo_with_uuid_name').attr('src', src + '?dbuuid=' + dbuuid + '&apps=' + apps);
                });
            }, 1500);
        },
    });
});
