# -*- coding: utf-8 -*-
{
    'name': "Odoo Data Migration",
    'summary': """
        This module can help you to migrate your data from your current system to Odoo database without RESTAPI,
        using database direct connection, this is very helpfull when your current system doesn't support RESTAPI technology.
        
        """,
    'description': """
        This module can help you to migrate your data from your current system to Odoo database without RESTAPI,
        using database direct connection, this is very helpfull when your current system doesn't support RESTAPI technology.
        
        This module will performs the migration process in a professional way using model objects, 
        in addition to that you can also use both systems (your current system and Odoo) together by 
        syncing Odoo with your old system,
        this is can done by defining schedule migration jobs to copy customers\vendors\products\inoices\.. data 
        to odoo based on Odoo schedule Actions.
    """,
    'author': "Bassam Mannaa",
    'website': "http://www.linkedin.com/in/bassam-mannaa-b8291a45",
    'category': 'tools',
    'version': '0.1',
    'license': 'OPL-1',
    'images': ['static/description/main_screenshot.png'],
    'depends': ['base'],
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/db_connection_view.xml',
        'views/menu.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}
