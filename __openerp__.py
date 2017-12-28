# -*- coding: utf-8 -*-
# Copyright 2017 Humanytek - Manuel Marquez <manuel@humanytek.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

{
    'name': 'Manager of Products Rotation',
    'version': '9.0.0.1.0',
    'category': 'Sales',
    'author': 'Humanytek',
    'website': "http://www.humanytek.com",
    'license': 'AGPL-3',
    'depends': [
        'product',
        'sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_rotation_view.xml',
        'views/product_view.xml',
    ],
    'installable': True,
    'auto_install': False
}
