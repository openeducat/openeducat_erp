# theme_web_openeducat – openEMIS UI Theme 🎨

## Overview

`theme_web_openeducat` is the custom Odoo web theme for openEMIS.  It applies the openEMIS branding (colours, logo, typography) across all backend and portal views.

---

## What It Changes

* Primary colour palette aligned with the openEMIS brand
* Custom top navigation bar and logo placement
* Login page branding
* Module icons and favicons

---

## Installation

This theme is bundled with the openEMIS ERP meta-module and installed automatically.  It can also be installed independently:

1. Place `theme_web_openeducat` in your Odoo addons directory.
2. Update the app list.
3. Install **openEMIS Web Theme**.

---

## Customisation

To apply your institution's own branding:

1. Override the SCSS variables in a child theme module.
2. Replace `static/img/logo.png` with your institution's logo.
3. Restart Odoo and regenerate assets.

---

## License

LGPL-3.0 – see repository [LICENSE](../LICENSE).
