from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_commission = fields.Boolean("Add Commission")