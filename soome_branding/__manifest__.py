{
    'name': 'SOOME Branding',
    'version': '17.0.1.0.0',
    'summary': 'Rebranding OpenEduCat vers SOOME',
    'depends': ['openeducat_core'],
    'data': [
        'data/ir_ui_menu.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'auto_install': True,
}
