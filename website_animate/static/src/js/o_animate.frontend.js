odoo.define('website_animate.o_animate_frontend', function (require) {
    'use strict';

    var s_animation = require('web_editor.snippets.animation');
    var base = require('web_editor.base');

    var WebsiteAnimate = {
        win   : {},
        items : {},

        offsetRatio : 0.3,  // Dynamic offset ratio: 0.3 = (element's height/3)
        offsetMin   : 10,   // Minimum offset for small elements (in pixels)

        // Retrieve animable elements and attach handlers.
        start: function () {
            var self   = this;
            self.items = $(".o_animate");
            self.items.each(function () {
                var $el = $(this);
                // Set all monitored elements to initial state
                self.reset_animation($el);
            });
            setTimeout(function () {
                self.attach_handlers();
            });
        },

        // Bind events and define the scrolling function
        attach_handlers: function () {
            var self = this;
            var lastScroll = 0;

            $(window)
            .on("resize.o_animate", function () {
                    self.win.h = $(window).height();
                    $(window).trigger("scroll");
            })
            .trigger("resize")
            .on("scroll.o_animate", (_.throttle(function () {
                // _.throttle -> Limit the number of times the scroll function
                // can be called in a given period. (http://underscorejs.org/#throttle)
                var windowTop    = $(window).scrollTop();
                var windowBottom = windowTop + self.win.h;

                // Handle reverse scrolling
                var direction = (windowTop < lastScroll) ? -1 : 1;
                lastScroll = windowTop;

                self.items.each(function () {
                    var $el       = $(this);
                    var elHeight  = $el.height();
                    var elOffset  = direction * Math.max((elHeight * self.offsetRatio), self.offsetMin)
                    var state     = $el.css("animation-play-state");

                    // We need to offset for the change in position from some animation
                    // So we get the top value of the transform matrix
                    var transformMatrix = $el.css('transform').replace(/[^0-9\-.,]/g, '').split(',')
                    var transformOffset = transformMatrix[13] || transformMatrix[5];
                    var elTop = $el.offset().top - transformOffset;

                    var visible = windowBottom > (elTop + elOffset) && windowTop < (elTop + elHeight - elOffset);

                    if ( visible && (state == "paused") ) {
                        $el.addClass("o_visible");
                        self.start_animation($el);
                    } else if ( !(visible) && $el.hasClass("o_animate_both_scroll") && (state == "running") ) {
                        $el.removeClass("o_visible");
                        self.reset_animation($el)
                    }
                });
            },100)))
            .trigger("scroll");
        },

        // Set elements to initial state
        reset_animation: function ($el) {
            var self = this;
            var anim_name = $el.css("animation-name");

            $el
            .css({"animation-name" : "dummy-none", "animation-play-state" : ""})
            .removeClass("o_animated o_animating")

            // force the browser to redraw using setTimeout
            setTimeout(function () {
                $el.css({"animation-name" : anim_name, "animation-play-state" : "paused"})
            },0);
        },

        // Start animation and/or update element's state
        start_animation: function ($el) {
            var self = this;

            // force the browser to redraw using setTimeout
            setTimeout(function () {
                $el
                .css({"animation-play-state": "running"})
                .addClass("o_animating")
                .one('webkitAnimationEnd oanimationend msAnimationEnd animationend', function (e) {
                    $el.addClass("o_animated").removeClass("o_animating");
                    $(window).trigger("resize");
                });
            });
        },
    };

    base.ready().then(function () {
        // By default, elements are hidden by the css of o_animate.
        // render alements  + // We will trigger the animation then pause it in state 0.
        WebsiteAnimate.start();
        // Then we render all the elements, the ones which are invisible
        // in state 0 (like fade_in for example) will stay invisible.
        $(".o_animate").css("visibility", "visible");
    });

    // Backward compatibility for enark animation system
    s_animation.registry.o_animate = s_animation.Class.extend({
        selector: '.o_animation',

        stop: function () {
            this._super();

            // Convert old classes to the new animation system
            var old_animation_classes = "o_animation o_displayed o_displayed_top o_displayed_middle o_displayed_bottom o_visible o_visible_top o_visible_middle o_visible_bottom";
            $(".o_fade_in").addClass("o_animate o_anim_fade_in").removeClass("o_fade_in");
            $(".o_fade_in_down").addClass("o_animate o_anim_fade_in_down").removeClass("o_fade_in_down");
            $(".o_fade_in_left").addClass("o_animate o_anim_fade_in_left").removeClass("o_fade_in_left");
            $(".o_fade_in_right").addClass("o_animate o_anim_fade_in_right").removeClass("o_fade_in_right");
            $(".o_fade_in_up").addClass("o_animate o_anim_fade_in_up").removeClass("o_fade_in_up");
            this.$target.removeClass(old_animation_classes);
        },
    });

    return WebsiteAnimate;
});
