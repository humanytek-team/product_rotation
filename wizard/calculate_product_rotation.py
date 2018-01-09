# -*- coding: utf-8 -*-
# Copyright 2017 Humanytek - Manuel Marquez <manuel@humanytek.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from datetime import datetime, timedelta
import hashlib

from openerp import api, fields, models, _
from openerp.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)


class CalculateProductRotation(models.TransientModel):
    _name = 'calculate.product.rotation'

    def _get_current_date(self):
        """Returns date with current day of the current month"""

        current_date = datetime.today().strftime('%Y-%m-%d')
        return current_date

    def _get_start_date(self):
        """Returns the default value of field start_date"""

        start_date = datetime.today() - timedelta(days=30)
        return start_date

    start_date = fields.Date('Start date of calculation',
                             required=True, default=_get_start_date)
    end_date = fields.Date('End date of calculation',
                           required=True, default=_get_current_date)
    company_id = fields.Many2one('res.company', 'Company')
    concept_id = fields.Many2one('product.style.concept', 'Concept')
    category_id = fields.Many2one('product.category', 'Category')
    percentage_denied = fields.Float('Percentage denied', default=100)

    @api.multi
    def calculate_products_rotation(self):
        """Calculates products rotation"""

        self.ensure_one()

        wizard = self
        wizard_hash = hashlib.md5(
            str(wizard.id) + wizard.start_date + wizard.end_date).hexdigest()

        ProductProduct = self.env['product.product']
        ProductRotation = self.env['product.rotation']
        ProductRotationParameter = self.env['product.rotation.parameter']
        SaleOrder = self.env['sale.order']

        products_domain = list()

        if self.concept_id:
            products_domain.append(
                ('product_style_concept_id', '=', self.concept_id.id))

        if self.category_id:
            products_domain.append(
                ('categ_id', '=', self.category_id.id))

        products = ProductProduct.search(products_domain)
        _logger.debug('DEBUG PRODUCTS DOMAIN %s', products_domain)
        _logger.debug('DEBUG PRODUCTS %s', products)

        domain_sales = [
            ('order_line.product_id.id', 'in', products.mapped('id')),
            ('date_order', '>=', self.start_date),
            ('date_order', '<=', self.end_date),
            ('state', 'in', ['sale', 'done']),
        ]

        if wizard.company_id:
            domain_sales.append(
                ('company_id', '=', wizard.company_id.id))

        sale_orders = SaleOrder.search(domain_sales)

        products_rotation = dict(
            (str(pr.id), dict([
                ('wizard_hash', wizard_hash),
                ('product_id', pr.id),
                ('start_date', wizard.start_date),
                ('end_date', wizard.end_date),
                ('company_id', wizard.company_id and wizard.company_id.id),
                ('concept_id', wizard.concept_id and wizard.concept_id.id),
                ('percentage_denied', wizard.percentage_denied),
            ])) for pr in products
        )

        for so in sale_orders:

            for line in so.order_line:

                if products_rotation.get(str(line.product_id.id), False) \
                        is not False:

                    if products_rotation[
                            str(line.product_id.id)].get(
                                'sales_quantity', False):

                        products_rotation[str(line.product_id.id)][
                            'sales_quantity'] += line.product_qty

                    else:
                        products_rotation[str(line.product_id.id)][
                            'sales_quantity'] = line.product_qty

        for product in products:

            rejected = product.products_rejected_ids.filtered(
                lambda r: r.date >= wizard.start_date and
                r.date <= wizard.end_date
            )

            if self.percentage_denied != 100:
                products_rotation[str(product.id)]['quantity_denied'] = sum(
                    rejected.mapped('qty')) * self.percentage_denied / 100.0

            else:
                products_rotation[str(product.id)]['quantity_denied'] = sum(
                    rejected.mapped('qty'))

            if products_rotation[str(product.id)].get('sales_quantity', False):
                products_rotation[str(product.id)]['demand'] = products_rotation[str(product.id)][
                    'sales_quantity'] + products_rotation[str(product.id)]['quantity_denied']

            else:
                products_rotation[str(product.id)]['demand'] = products_rotation[
                    str(product.id)]['quantity_denied']

        total_demand = float(sum([products_rotation[product_id]['demand']
                                  for product_id in products_rotation]))

        if total_demand == 0:
            raise ValidationError(
                _('There was no demand for products in this period.'))

        _logger.debug('DEBUG TOTAL DEMAND %s', total_demand)
        for product in products:
            _logger.debug('DEBUG PRODUCT ID %s', product.id)
            _logger.debug('DEBUG PRODUCT DEMAND %s',
                          products_rotation[str(product.id)]['demand'])
            products_rotation[str(product.id)].update({
                'total_demand': total_demand,
                'participation': (
                    products_rotation[str(product.id)]['demand'] * 100
                ) / total_demand
            })

        products_rotation_sorted = sorted(
            products_rotation.items(),
            key=lambda x: x[1]['participation'],
            reverse=True)

        rotation_rate_previous_product = 0
        product_rotation_parameters = ProductRotationParameter.search([])

        for product_rotation in products_rotation_sorted:

            if rotation_rate_previous_product == 0:

                products_rotation[product_rotation[0]][
                    'rotation_rate'] = products_rotation[product_rotation[0]][
                        'participation']

            else:
                products_rotation[product_rotation[0]][
                    'rotation_rate'] = products_rotation[
                        product_rotation[0]]['participation'] + \
                    rotation_rate_previous_product

                product_rotation_parameter = product_rotation_parameters.filtered(
                    lambda p: products_rotation[product_rotation[0]]['rotation_rate'] >=
                    p.limit_lower
                    and
                    products_rotation[product_rotation[0]]['rotation_rate'] <=
                    p.limit_upper
                )

                if product_rotation_parameter:
                    products_rotation[product_rotation[0]][
                        'product_rotation_parameter_id'] = product_rotation_parameter[0].id

            rotation_rate_previous_product = products_rotation[
                product_rotation[0]]['rotation_rate']

        first_and_second_pr = [pr[0] for pr in products_rotation_sorted][:2]

        products_rotation[first_and_second_pr[0]]['rotation_rate'] = products_rotation[
            first_and_second_pr[1]]['rotation_rate']

        products_rotation[first_and_second_pr[0]][
            'product_rotation_parameter_id'] = products_rotation[first_and_second_pr[1]][
                'product_rotation_parameter_id']

        for product_id in products_rotation:

            ProductRotation.create(products_rotation[product_id])

            ProductProduct.browse(int(product_id)).write(
                {'current_rotation': products_rotation[
                    product_id]['product_rotation_parameter_id']})

        return {
            'name': _('Products Rotation'),
            'context': self._context,
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': 'product.rotation',
            'type': 'ir.actions.act_window',
            'domain': [('wizard_hash', '=', wizard_hash)],
        }
