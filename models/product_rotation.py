# -*- coding: utf-8 -*-
# Copyright 2017 Humanytek - Manuel Marquez <manuel@humanytek.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from openerp import api, fields, models


class ProductRotationParameter(models.Model):
    _name = 'product.rotation.parameter'

    name = fields.Char('Value', required=True)
    limit_lower = fields.Float('Limit Lower (percentage)', required=True)
    limit_upper = fields.Float('Limit Upper (percentage)', required=True)


class ProductRotation(models.Model):
    _name = 'product.rotation'
    _rec_name = 'product_rotation_parameter_id'
    _order = 'rotation_rate'

    product_rotation_parameter_id = fields.Many2one(
        'product.rotation.parameter', 'Rotation', required=True)
    start_date = fields.Date('Start date of calculation', required=True)
    end_date = fields.Date('End date of calculation', required=True)
    product_id = fields.Many2one('product.product', 'Product', required=True)
    company_id = fields.Many2one('res.company', 'Company')
    concept_id = fields.Many2one('product.style.concept', 'Concept')
    percentage_denied = fields.Float('Percentage denied', default=100)
    sales_quantity = fields.Float('Sales Quantity')
    quantity_denied = fields.Float('Quantity Denied')
    demand = fields.Float('Demand')
    total_demand = fields.Float('Total Demand')
    participation = fields.Float('Participation (percentage)')
    rotation_rate = fields.Float('Rotation Rate')
    wizard_hash = fields.Char('Wizard Hash')
