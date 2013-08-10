openerp.openeducat_erp = function(instance) {
    var QWeb = instance.web.qweb;
    var _t = instance.web._t;

instance.web.WebClient = instance.web.Client.extend({
    _template: 'WebClient',
    events: {
        'click .oe_logo_edit_admin': 'logo_edit'
    },
    init: function(parent) {
        this._super(parent);
        this._current_state = null;
        this.menu_dm = new instance.web.DropMisordered();
        this.action_mutex = new $.Mutex();
    },
    start: function() {
        var self = this;
        return $.when(this._super()).then(function() {
            if (jQuery.param !== undefined && jQuery.deparam(jQuery.param.querystring()).kitten !== undefined) {
                $("body").addClass("kitten-mode-activated");
                $("body").css("background-image", "url(" + instance.session.origin + "/web/static/src/img/back-enable.jpg" + ")");
                if ($.blockUI) {
                    $.blockUI.defaults.message = '<img src="http://www.amigrave.com/kitten.gif">';
                }
            }
            if (!self.session.session_is_valid()) {
                self.show_login();
            } else {
                self.show_application();
            }
        });
    },
    set_title: function(title) {
        title = _.str.clean(title);
        var sep = _.isEmpty(title) ? '' : ' - ';
        document.title = title + sep + 'OpenEduCat';
    },
    show_common: function() {
        var self = this;
        this._super();
        window.onerror = function (message, file, line) {
            self.crashmanager.show_error({
                type: _t("Client Error"),
                message: message,
                data: {debug: file + ':' + line}
            });
        };
    },
    show_login: function() {
        this.toggle_bars(false);

        var state = $.bbq.getState(true);
        var action = {
            type: 'ir.actions.client',
            tag: 'login',
            _push_me: false,
        };

        this.action_manager.do_action(action);
        this.action_manager.inner_widget.on('login_successful', this, function() {
            this.show_application();        // will load the state we just pushed
        });
    },
    show_application: function() {
        var self = this;
        self.toggle_bars(true);
        self.update_logo();
        self.menu = new instance.web.Menu(self);
        self.menu.replace(this.$el.find('.oe_menu_placeholder'));
        self.menu.on('menu_click', this, this.on_menu_action);
        self.user_menu = new instance.web.UserMenu(self);
        self.user_menu.replace(this.$el.find('.oe_user_menu_placeholder'));
        self.user_menu.on('user_logout', self, self.on_logout);
        self.user_menu.do_update();
        self.bind_hashchange();
        self.set_title();
        self.check_timezone();
    },
    update_logo: function() {
        var img = this.session.url('/web/binary/company_logo');
        this.$('.oe_logo img').attr('src', '').attr('src', img);
        this.$('.oe_logo_edit').toggleClass('oe_logo_edit_admin', this.session.uid === 1);
    },
    logo_edit: function(ev) {
        var self = this;
        self.alive(new instance.web.Model("res.users").get_func("read")(this.session.uid, ["company_id"])).then(function(res) {
            self.rpc("/web/action/load", { action_id: "base.action_res_company_form" }).done(function(result) {
                result.res_id = res['company_id'][0];
                result.target = "new";
                result.views = [[false, 'form']];
                result.flags = {
                    action_buttons: true,
                };
                self.action_manager.do_action(result);
                var form = self.action_manager.dialog_widget.views.form.controller;
                form.on("on_button_cancel", self.action_manager.dialog, self.action_manager.dialog.close);
                form.on('record_saved', self, function() {
                    self.action_manager.dialog.close();
                    self.update_logo();
                });
            });
        });
        return false;
    },
    check_timezone: function() {
        var self = this;
        return self.alive(new instance.web.Model('res.users').call('read', [[this.session.uid], ['tz_offset']])).then(function(result) {
            var user_offset = result[0]['tz_offset'];
            var offset = -(new Date().getTimezoneOffset());
            // _.str.sprintf()'s zero front padding is buggy with signed decimals, so doing it manually
            var browser_offset = (offset < 0) ? "-" : "+";
            browser_offset += _.str.sprintf("%02d", Math.abs(offset / 60));
            browser_offset += _.str.sprintf("%02d", Math.abs(offset % 60));
            if (browser_offset !== user_offset) {
                var $icon = $(QWeb.render('WebClient.timezone_systray'));
                $icon.on('click', function() {
                    var notification = self.do_warn(_t("Timezone Mismatch"), QWeb.render('WebClient.timezone_notification', {
                        user_timezone: instance.session.user_context.tz || 'UTC',
                        user_offset: user_offset,
                        browser_offset: browser_offset,
                    }), true);
                    notification.element.find('.oe_webclient_timezone_notification').on('click', function() {
                        notification.close();
                    }).find('a').on('click', function() {
                        notification.close();
                        self.user_menu.on_menu_settings();
                        return false;
                    });
                });
                $icon.appendTo(self.$('.oe_systray'));
            }
        });
    },
    destroy_content: function() {
        _.each(_.clone(this.getChildren()), function(el) {
            el.destroy();
        });
        this.$el.children().remove();
    },
    do_reload: function() {
        var self = this;
        return this.session.session_reload().then(function () {
            instance.session.load_modules(true).then(
                self.menu.proxy('do_reload')); });

    },
    do_notify: function() {
        var n = this.notification;
        return n.notify.apply(n, arguments);
    },
    do_warn: function() {
        var n = this.notification;
        return n.warn.apply(n, arguments);
    },
    on_logout: function() {
        var self = this;
        if (!this.has_uncommitted_changes()) {
            this.session.session_logout().done(function () {
                $(window).unbind('hashchange', self.on_hashchange);
                self.do_push_state({});
                window.location.reload();
            });
        }
    },
    bind_hashchange: function() {
        var self = this;
        $(window).bind('hashchange', this.on_hashchange);

        var state = $.bbq.getState(true);
        if (_.isEmpty(state) || state.action == "login") {
            self.menu.has_been_loaded.done(function() {
                var first_menu_id = self.menu.$el.find("a:first").data("menu");
                if(first_menu_id) {
                    self.menu.menu_click(first_menu_id);
                }
            });
        } else {
            $(window).trigger('hashchange');
        }
    },
    on_hashchange: function(event) {
        var self = this;
        var stringstate = event.getState(false);
        if (!_.isEqual(this._current_state, stringstate)) {
            var state = event.getState(true);
            if(!state.action && state.menu_id) {
                self.menu.has_been_loaded.done(function() {
                    self.menu.do_reload().done(function() {
                        self.menu.menu_click(state.menu_id);
                    });
                });
            } else {
                state._push_me = false;  // no need to push state back...
                this.action_manager.do_load_state(state, !!this._current_state);
            }
        }
        this._current_state = stringstate;
    },
    do_push_state: function(state) {
        this.set_title(state.title);
        delete state.title;
        var url = '#' + $.param(state);
        this._current_state = $.deparam($.param(state), false);     // stringify all values
        $.bbq.pushState(url);
        this.trigger('state_pushed', state);
    },
    on_menu_action: function(options) {
        var self = this;
        return this.menu_dm.add(this.rpc("/web/action/load", { action_id: options.action_id }))
            .then(function (result) {
                return self.action_mutex.exec(function() {
                    if (options.needaction) {
                        result.context = new instance.web.CompoundContext(result.context, {
                            search_default_message_unread: true,
                            search_disable_custom_filters: true,
                        });
                    }
                    var completed = $.Deferred();
                    $.when(self.action_manager.do_action(result, {
                        clear_breadcrumbs: true,
                        action_menu_id: self.menu.current_menu,
                    })).fail(function() {
                        self.menu.open_menu(options.previous_menu_id);
                    }).always(function() {
                        completed.resolve();
                    });
                    setTimeout(function() {
                        completed.resolve();
                    }, 2000);
                    // We block the menu when clicking on an element until the action has correctly finished
                    // loading. If something crash, there is a 2 seconds timeout before it's unblocked.
                    return completed;
                });
            });
    },
    set_content_full_screen: function(fullscreen) {
        $(document.body).css('overflow-y', fullscreen ? 'hidden' : 'scroll');
        this.$('.oe_webclient').toggleClass(
            'oe_content_full_screen', fullscreen);
    },
    has_uncommitted_changes: function() {
        var $e = $.Event('clear_uncommitted_changes');
        instance.web.bus.trigger('clear_uncommitted_changes', $e);
        if ($e.isDefaultPrevented()) {
            return true;
        } else {
            return this._super.apply(this, arguments);
        }
    },
});


};

// vim:et fdc=0 fdl=0 foldnestmax=3 fdm=syntax:
