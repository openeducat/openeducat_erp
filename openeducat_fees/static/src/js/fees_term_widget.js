/** @odoo-module **/

import {standardFieldProps} from '@web/views/fields/standard_field_props';
import {registry} from '@web/core/registry';
import { Component, useProps } from "@odoo/owl";

export class FeesTermsDisplay extends Component {
    static template = "website.FieldFeesTermsDisplay";
    props = useProps(standardFieldProps);

    get terms() {
        const selection = this.props.record.fields[this.props.name].selection;
        return selection.filter(item => item[0] || item[1]).map(item => ({
            value: item[0],
            label: item[1],
            description: this.props.record.data.fees_terms_description || ''
        }));
    }
    _onClickLabel(value) {
        this.props.record.update({ [this.props.name]: value });
    }

     get description() {
         return {
            'fixed_days': 'Fixed fee per attendance day.',
            'fixed_date': 'Fixed fee for a specific period or dates.',
            'duration_based': 'Fees based on session or program length.',
            'session_based': 'Fee per session; pay-as-you-go.',
            'faculty_based': 'Fees depends on faculty expertise and specialization.'
        }
     }
    get ImagePath() {
        return {
            'fixed_days': '/openeducat_fees/static/description/term_type_1.svg',
            'fixed_date': '/openeducat_fees/static/description/term_type_2.svg',
            'duration_based': '/openeducat_fees/static/description/term_type_3.svg',
            'session_based': '/openeducat_fees/static/description/term_type_4.svg',
            'faculty_based': '/openeducat_fees/static/description/term_type_5.svg'
        }
    }
    onSelectValue(value) {
        this.props.record.update({ [this.props.name]: value });
    }
}

export const feesTermsDisplay = {
    component: FeesTermsDisplay,
    supportedTypes: ['selection'],
};

registry.category("fields").add("fees_terms_display", feesTermsDisplay);
