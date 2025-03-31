{
    'name': 'OpenEduCat Demo Theme',
    'description': 'OpenEduCat Demo Theme',
    'category': 'Theme',
    'version': '18.0',
    'author': 'OpenEduCat',
    'depends': [
        'website',
        'theme_default',
        'website_mass_mailing'
    ],
    'data': [
        'views/homepage.xml',
        'views/web.xml',

        # 'views/templates.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            '/theme_web_openeducat/static/src/scss/primary_variables.scss',
        ],
        'web.assets_frontend': [
            '/theme_web_openeducat/static/src/scss/style.scss',
            '/theme_web_openeducat/static/src/js/home.js',
        ],
    },
    'license': 'LGPL-3',
    'application': 'true'
}
##############################################################################
