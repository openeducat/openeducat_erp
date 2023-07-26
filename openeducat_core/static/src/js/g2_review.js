odoo.define('openeducat_core.g2_review', function (require) {
    "use strict";

    var core = require('web.core');
    var Dialog = require("web.Dialog");
    var session = require('web.session');
    var ajax = require('web.ajax');
    var QWeb = core.qweb;
    const utils = require('web.utils');

    $(document).ready(function(){

        const nbDays = 7;
        const reviewShow = !!utils.get_cookie(`g2_review_${session.db}`);

        if(!reviewShow){
            setTimeout(async () => {
                await ajax.loadXML('/openeducat_core/static/src/xml/review.xml', QWeb);
                var review_dialog = new Dialog(null, {
                    title: 'G2 Review',
                    size: 'medium',
                    dialogClass: 'g2_review_dialog',
                    renderFooter: false,
                    renderHeader: false,
                    $parentNode: $(document.body),
                    $content: $(QWeb.render('openeducat_core.review_dialog')),
                });
                review_dialog.open();
                review_dialog.opened().then(function(){
                    review_dialog.$modal.find('.modal-dialog').addClass('modal-dialog-centered');
                    review_dialog.$modal.find('.modal-body').removeClass('modal-body');
                    review_dialog.$el.find('#write_g2_review').on('click', (e) => {
                        e.preventDefault();
                        window.open('https://openeducat.org/g2feedback', '_blank');
                        review_dialog.close();

                        utils.set_cookie(`g2_review_${session.db}`, true, nbDays * 24 * 60 * 60);
                    });
                    review_dialog.$el.find('.js_close_popup').on('click', (e) => {
                        review_dialog.close();

                        utils.set_cookie(`g2_review_${session.db}`, true, nbDays * 24 * 60 * 60);
                    });
                });
            }, 5000);
        }
    });
});