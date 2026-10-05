import { patch } from "@web/core/utils/patch";
import { CalendarCommonPopover } from "@web/views/calendar/calendar_common/calendar_common_popover";

/**
 * Tag the event popover of OpenEduCat calendars (op.* models) so the close
 * button can be laid out inside the header (see op_calendar_popover.scss).
 * Done as a patch rather than a js_class so it also applies to calendars
 * whose view class is replaced by another module.
 */
patch(CalendarCommonPopover.prototype, {
    get cardPopoverProps() {
        const props = super.cardPopoverProps;
        if (!this.props.model.resModel?.startsWith("op.")) {
            return props;
        }
        return { ...props, rootClass: `${props.rootClass} o_op_calendar_popover` };
    },
});
