# -*- coding: utf-8 -*-
# Copyright 2017 Humanytek - Manuel Marquez <manuel@humanytek.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from openerp import fields, models


class ProductRotationParameter(models.Model):
    _name = 'product.rotation.parameter'

    name = fields.Char('Value', required=True)
    limit_lower = fields.Float('Limit Lower (percentage)', required=True)
    limit_upper = fields.Float('Limit Upper (percentage)', required=True)
