/** @odoo-module **/

// Odoo 20 / Owl 3 treats `t-att-style` in the "board.arch" template as a CSS
// binding and drops a value like "2-1", so every save of My Dashboard wrote
// `<board>` without its layout and the next load crashed in BoardArchParser
// (`layout.split` on null). Put the layout back when saving, and fall back to
// the default layout for dashboards already saved without it.
import { patch } from "@web/core/utils/patch";
import { rpc, rpcBus } from "@web/core/network/rpc";
import { renderToFragment } from "@web/core/utils/render";
import { parseXML } from "@web/core/utils/xml";
import { BoardController } from "@board/board_controller";
import { BoardArchParser } from "@board/board_view";

const DEFAULT_LAYOUT = "2-1";
const xmlSerializer = new XMLSerializer();

patch(BoardController.prototype, {
    saveBoard() {
        const root = document.createElement("rendertostring");
        root.appendChild(renderToFragment("board.arch", this.board));
        const board = root.querySelector("board");
        if (board) {
            board.setAttribute("style", this.board.layout || DEFAULT_LAYOUT);
        }
        const result = xmlSerializer.serializeToString(root);
        const arch = result.slice(result.indexOf("<", 1), result.indexOf("</rendertostring>"));

        rpc("/web/view/edit_custom", {
            custom_id: this.board.customViewId,
            arch,
        });
        rpcBus.trigger("CLEAR-CACHES");
    },
});

patch(BoardArchParser.prototype, {
    parse(arch, customViewId) {
        const xml = typeof arch === "string" ? parseXML(arch) : arch;
        for (const board of xml.querySelectorAll("board")) {
            if (!board.getAttribute("style")) {
                board.setAttribute("style", DEFAULT_LAYOUT);
            }
        }
        return super.parse(xml, customViewId);
    },
});
