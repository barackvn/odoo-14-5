# -*- coding: utf-8 -*-
{
    'name': "QR Code Generator",
    'summary': """Integrated QR code generator within the odoo framework.""",
    'description': """Helps to generate QR codes for texts or large urls.""",
    'version': '14.0.1.0.0',
    'category': 'Tools',
    'author': "Kripal K",
    'website': "https://www.linkedin.com/in/kripal754/",
    'license': 'LGPL-3',
    'depends': ['base', 'web'],
    'qweb': ['static/src/xml/qr_generator.xml'],
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
