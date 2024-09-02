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

    }
});
