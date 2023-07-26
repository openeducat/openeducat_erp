/** @odoo-module **/

import { session } from "@web/session";
import Dialog from 'web.Dialog';
import core from 'web.core';
const QWeb = core.qweb;
import { getCookie, setCookie } from 'web.utils.cookies';

$(document).ready(function(){

    const nbDays = 7;
    const reviewShow = !!getCookie(`g2_review_${session.db}`);

    if(!reviewShow){
        setTimeout(() => {

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

                    setCookie(`g2_review_${session.db}`, true, nbDays * 24 * 60 * 60, 'required');
                });
                review_dialog.$el.find('.js_close_popup').on('click', (e) => {
                    review_dialog.close();

                    setCookie(`g2_review_${session.db}`, true, nbDays * 24 * 60 * 60, 'required');
                });
            });
        }, 5000);
    }
});
