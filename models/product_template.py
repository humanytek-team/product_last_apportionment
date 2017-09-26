from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    last_apportionment = fields.Date()
    last_usd_cost = fields.Monetary()
