odoo.define('website_animate.o_animate_editor', function (require) {
    'use strict';

    var s_options = require('web_editor.snippets.options');

    //  Animations
    s_options.registry.o_animate = s_options.Class.extend({
        start: function () {
            this._super();
            var self = this;

            setTimeout(function () {

                if (self.$overlay.find("li.snippet-option-o_animate > ul > li li.active").length > 0) {
                    self.update_options_visibility("show");
                } else {
                    self.update_options_visibility("hide");
                }

                // remove theme_enark animation options from the context menu
                // WARNING: theme_enark do not prefix js methods,
                // Remove in Odoo9

                if (self.$overlay.find('li.snippet-option-animation').length > 0) {
                    $(this).addClass("hidden");
                }

            }, 500)
        },

        select_class: function (type, value, $li) {
            this._super(type, value, $li);
            var self = this;

            setTimeout(function () {
                self.$target.addClass("o_animate_preview o_animate").css('animation-name', 'dummy-none');
                self.$target.css('animation-name', '');
            });

            if (type != "click") {return}
            if (value.length > 0 ) {
                self.update_options_visibility("show");
                self.$target.removeClass("o_animate_preview");
            } else {
                setTimeout(function () {
                    self.update_options_visibility("hide");
                    self.$target.removeClass("o_animate_preview o_animate");
                }, 500)
            }
        },

        update_options_visibility: function (value) {
            var self = this;
            var opts = ".snippet-option-o_animate_duration, .snippet-option-o_animate_delay, .snippet-option-o_animate_options";
            setTimeout(function () {
                if (value == "show") {
                    self.$overlay.find(opts).removeClass("hidden");
                } else if (value == "hide") {
                    self.$overlay.find(opts).addClass("hidden");
                }
            })
        },

        clean_for_save: function () {
            var self = this;

            // Clean elements
            self.$target
            .removeClass("o_animating o_animated o_animate_preview")
            .css({
                'animation': '',
                'animation-name': '',
                'animation-play-state': '',
                'visibility': ''
            });
            if (self.$target.hasClass("o_animate")) {
                self.$target.css('animation-play-state', 'paused');
            }

            // Clean all inView elements
            $("#wrapwrap").find(".o_animate").removeClass("o_visible");
        },
    });

    // Duration
    s_options.registry.o_animate_duration = s_options.Class.extend({
        select_class: function (type, value, $li) {
            this._super(type, value, $li);

            var self = this;
            var $timeline_duration = self.$overlay.find(".timeline.duration span[simulate='duration']");
            var $timeline_delay    = self.$overlay.find(".timeline.duration span[simulate='delay']");

            self.$target
            .css({
                'animation-duration': '',
                'animation-delay': ''
            });

            var el_delay    = self.$target.css("animation-delay");
            var el_duration = self.$target.css("animation-duration");
            var el_period;

            el_delay = parseFloat(el_delay.slice(0,-1));
            el_duration = parseFloat(el_duration.slice(0,-1));
            el_period = el_delay + el_duration;

            $timeline_duration.parent().width((el_duration*100)/el_period +"%");
            $timeline_delay.parent().width((el_delay*100)/el_period +"%");

            self.$target.addClass("o_animate_preview").css('animation-name', 'dummy-none').css('animation-duration', '0s');

            $timeline_duration.css('animation-name', 'dummy-none').css('animation-duration', el_duration + "s").css('animation-delay', el_delay  + "s");
            $timeline_delay.css('animation-name', 'dummy-none').css('animation-duration', el_delay  + "s");

            setTimeout(function () {
                self.$target.css('animation-name', '').css('animation-duration', '');

                $timeline_duration.css('animation-name', '');
                $timeline_delay.css('animation-name', '');
            });
        },
    });

    // Delay
    s_options.registry.o_animate_delay = s_options.Class.extend({
        select_class: function (type, value, $li) {
            this._super(type, value, $li);
            var self = this;
            var $timeline_delay = self.$overlay.find(".timeline.delay span[simulate='delay']");
            var $timeline_duration = self.$overlay.find(".timeline.delay span[simulate='duration']");

            self.$target
            .css({
                'animation-duration': '',
                'animation-delay': ''
            });

            var el_delay    = self.$target.css("animation-delay");
            var el_duration = self.$target.css("animation-duration");
            var el_period;

            el_delay = parseFloat(el_delay.slice(0,-1));
            el_duration = parseFloat(el_duration.slice(0,-1));
            el_period = el_delay + el_duration;

            $timeline_duration.parent().width((el_duration*100)/el_period +"%");
            $timeline_delay.parent().width((el_delay*100)/el_period +"%");

            self.$target.addClass("o_animate_preview").css('animation-name', 'dummy-none').css('animation-duration', '0s');

            $timeline_duration.css('animation-name', 'dummy-none').css('animation-duration', el_duration + "s").css('animation-delay', el_delay  + "s");
            $timeline_delay.css('animation-name', 'dummy-none').css('animation-duration', el_delay  + "s");

            setTimeout(function () {
                self.$target.css('animation-name', '').css('animation-duration', '');

                $timeline_duration.css('animation-name', '');
                $timeline_delay.css('animation-name', '');
            });
        },
    });
});
