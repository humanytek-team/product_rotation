# -*- coding: utf-8 -*-
# Copyright 2017 Humanytek - Manuel Marquez <manuel@humanytek.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from openerp import fields, models


class ProductRotation(models.Model):
    _inherit = 'product.product'

    rotation_history_ids = fields.One2many(
        'product.rotation', 'product_id', 'Product Rotation History')
    current_rotation = fields.Many2one(
        'product.rotation.parameter', 'Current Rotation', readonly=True)
