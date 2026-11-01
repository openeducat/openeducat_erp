# 1. Pulls the official Odoo base system with all system dependencies pre-installed
FROM odoo:17.0

# 2. Copies your downloaded OpenEduCat source folders directly into Odoo's custom addons path
COPY ./ /mnt/extra-addons/

# 3. Switches the active user container back to Odoo's secure profile
USER odoo

# 4. Boots the system and opens the web application port
CMD ["odoo", "--http-port=8069"]
