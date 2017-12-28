# -*- coding: utf-8 -*-
# Copyright 2017 Humanytek - Manuel Marquez <manuel@humanytek.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from openerp import fields, models


class ProductRotationParameter(models.Model):
    _name = 'product.rotation.parameter'

    name = fields.Char('Value', required=True)
    limit_lower = fields.Float('Limit Lower (percentage)', required=True)
    limit_upper = fields.Float('Limit Upper (percentage)', required=True)


class ProductRotation(models.Model):
    _name = 'product.rotation'

    product_rotation_parameter_id = fields.Many2one(
        'product.rotation.parameter', 'Rotation', required=True)
    start_date = fields.Date('Start date of calculation', required=True)
    end_date = fields.Date('End date of calculation', required=True)
    product_id = fields.Many2one('product.product', 'Product', required=True)
