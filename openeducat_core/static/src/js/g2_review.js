/** @odoo-module **/

import { session } from "@web/session";
import { Dialog } from "@web/core/dialog/dialog";
import { useService } from "@web/core/utils/hooks";
import { WebClient } from "@web/webclient/webclient";
import { Component, xml } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { cookie } from "@web/core/browser/cookie";

export class G2ReviewDialog extends Component {
    setup() {
        this.nbDays = 7;
        this.title = 'G2 Review'
    }
    onClickG2Review() {
        window.open('https://www.openeducat.org/g2feedback', '_blank');
        this.props.close();
        cookie.set(`g2_review_${session.db}`, true, this.nbDays * 24 * 60 * 60, 'required');
    }
    onClose() {
        this.props.close();
        cookie.set(`g2_review_${session.db}`, true, this.nbDays * 24 * 60 * 60, 'required');
    }
}
G2ReviewDialog.components = { Dialog };
G2ReviewDialog.template = 'openeducat_core.g2_review_dialog'
G2ReviewDialog.props = {
    close: Function,
};

export class G2Review extends Component {
    setup() {
        const reviewShow = !!cookie.get(`g2_review_${session.db}`);
        this.dialog = useService("dialog");

        if (!reviewShow) {
            setTimeout(() => {
                this.dialog.add(G2ReviewDialog );
            }, 5000);
        }
    }
}
G2Review.template = xml``;

WebClient.components = {
    ...WebClient.components,
    G2Review
}
return G2ReviewDialog;
