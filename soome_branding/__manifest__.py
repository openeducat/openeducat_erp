{
    'name': 'SOOME Branding',
    'version': '17.0.1.0.0',
    'summary': 'Rebranding OpenEduCat vers SOOME',
    'depends': ['openeducat_core', 'web'],
    'data': [
        'data/ir_ui_menu.xml',
        'views/database_selector.xml',
    ],
    'assets': {
        'web.assets_common': [
            'soome_branding/static/src/css/database_selector.css',
        ],
    },
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'auto_install': True,
}
