#!/bin/bash
echo "🎨 Application des patches SOOME..."

ODOO=$HOME/odoo17
PATCHES=/workspaces/soome_erp/scripts/patches
BRANDING=/workspaces/soome_erp/soome_branding/static/src/img

# Copier les fichiers patchés
cp $PATCHES/database_manager.qweb.html $ODOO/addons/web/static/src/public/database_manager.qweb.html
cp $PATCHES/webclient.js $ODOO/addons/web/static/src/webclient/webclient.js
cp $PATCHES/webclient_templates.xml $ODOO/addons/web/views/webclient_templates.xml
cp $PATCHES/bootstrap.css $ODOO/addons/web/static/lib/bootstrap/dist/css/bootstrap.css

# Remplacer le logo
cp $BRANDING/soome_logo2.png $ODOO/addons/web/static/img/logo.png

echo "✅ Patches SOOME appliqués !"
