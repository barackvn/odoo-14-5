# -*- coding: utf-8 -*-
{
    'name': "Hotel Custom",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Marina Boules",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hotel', 'hotel_management'],

    # always loaded
    'data': [
        # 'security/user_security.xml',
        # 'security/ir.model.access.csv',
        'views/res_partner_view.xml',
        'views/room_view.xml',
        'views/hotel_reservation_line_view.xml',
    ],
}
