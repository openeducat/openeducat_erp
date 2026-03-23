{
    'name': 'SOOME Theme',
    'version': '17.0.1.0.0',
    'summary': 'Theme global SOOME',
    'depends': ['web'],
    'data': [
        'views/login_layout.xml',
    ],
    'assets': {
        'web.assets_common': [
            'soome_theme/static/src/css/soome.css',
        ],
    },
    'installable': True,
    'auto_install': False,
}
