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

    @api.multi
    def _get_display_price(self, product):
        # TO DO: move me in master/saas-16 on sale.order
        if self.order_id.pricelist_id.discount_policy == 'with_discount':
            pricelist_item = False
            for line in self.order_id.pricelist_id.item_ids:
                if line.categ_id == product.categ_id:
                    pricelist_item = line
                    break
            if pricelist_item and pricelist_item.fir:
                fir = pricelist_item.fir
                financial_cost = self.last_usd_cost * fir
                total_cost = self.last_usd_cost + financial_cost
                return total_cost / (1 - pricelist_item.gain/100)
            else:
                return product.with_context(pricelist=self.order_id.pricelist_id.id).price
        price, rule_id = self.order_id.pricelist_id.get_product_price_rule(self.product_id, self.product_uom_qty or 1.0, self.order_id.partner_id)
        pricelist_item = self.env['product.pricelist.item'].browse(rule_id)
        if (pricelist_item.base == 'pricelist' and pricelist_item.base_pricelist_id.discount_policy == 'with_discount'):
            price, rule_id = pricelist_item.base_pricelist_id.get_product_price_rule(self.product_id, self.product_uom_qty or 1.0, self.order_id.partner_id)
            return price
        else:
            from_currency = self.order_id.company_id.currency_id
            return from_currency.compute(product.lst_price, self.order_id.pricelist_id.currency_id)
