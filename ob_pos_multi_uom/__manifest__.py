# -*- coding: utf-8 -*-

{
    'name': "POS Multi UOM",
    'summary': """
        Helps to change UOM in POS. Only UOMs in same category of base UOM will be shown.""",
    'description': """
        Helps to change UOM in POS. Only UOMs in same category of base UOM will be shown.""",
    'author': "Odoo Being",
    'website': "https://www.odoobeing.com",
    'license': 'AGPL-3',
    'category': 'Point of Sale',
    'images': ['static/description/images/pos_multi_uom_banner.png'],
    'version': '14.0.0.1',
    'support': 'odoobeing@gmail.com',
    'depends': ['point_of_sale'],
    'data': [
        'views/pos_assets.xml',
        'views/pos_order.xml',
        'views/pos_config.xml',
    ],
    'qweb': [
        'static/src/xml/multi_uom.xml',
    ],
    'installable': True,
    'auto_install': False,
}
