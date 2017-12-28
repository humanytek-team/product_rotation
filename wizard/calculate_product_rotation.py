# -*- coding: utf-8 -*-
# Copyright 2017 Humanytek - Manuel Marquez <manuel@humanytek.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from datetime import datetime, timedelta

from openerp import fields, models


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
    percentage_denied = fields.Float('Percentage denied', default=100)
