from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_commission = fields.Boolean("Add Commission")
    total_commission = fields.Float(compute="_compute_total_commission", string="Total Commission: ")

    @api.depends("order_line.commission", "is_commission")
    def _compute_total_commission(self):
         for order in self:
            if order.is_commission:
                order.total_commission = sum(order.order_line.mapped('commission'))
            else:
                order.total_commission = 0.0