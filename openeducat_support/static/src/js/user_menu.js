odoo.define('web_user_menu', function(require) {
    "use strict";

    var UserMenu = require('web.UserMenu');

    UserMenu.include({
        on_menu_documentation: function() {
            window.open('http://doc.openeducat.org/', '_blank');
        },
        on_menu_support: function() {
            window.open('https://www.openeducat.org/page/support', '_blank');
        },
        on_menu_account: function() {
            window.open('https://www.openeducat.org/web/login', '_blank');
        },
    });
});
