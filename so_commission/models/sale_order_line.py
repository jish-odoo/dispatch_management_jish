from odoo import models, fields

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    commission = fields.Integer("Commission")

    
        

