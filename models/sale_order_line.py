from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    last_apportionment = fields.Date(
        readonly=True,
        related='product_id.last_apportionment',
    )
    last_usd_cost = fields.Monetary(
        readonly=True,
        related='product_id.last_usd_cost',
    )
