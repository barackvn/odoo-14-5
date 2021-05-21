# -*- coding: utf-8 -*-
{
    'name': "Product UoM Category",

    'summary': """
        This module will allow you to assign UoM category in product template and it
        will filter the list of default UoM and purchase UoM.""",

    'description': """
        This module will allow you to assign UoM category in product template and it
        will filter the list of default UoM and purchase UoM.
    """,

    'author': 'CorTex IT Solutions Ltd.',
    'website': 'https://cortexsolutions.net',
    'license': 'OPL-1',
    'category': 'Inventory',
    'version': '1.0.0',
    'installable': True,
    'auto_install': False,
    # any module necessary for this one to work correctly
    'depends': ['stock'],
    'post_init_hook': 'post_init_hook',
    'images': ['static/description/main_screenshot.png'],

    # always loaded
    'data': [
        'views/uom_category_views.xml',
    ],
}
