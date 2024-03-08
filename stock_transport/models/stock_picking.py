from odoo import fields, models, api

class StockPicking(models.Model):
    _inherit = "stock.picking"

    shipped_volume = fields.Float(compute="compute_total_weight_volume")
    shipped_weight = fields.Float(compute="compute_total_weight_volume")
    
        
    @api.depends("move_line_ids")
    def compute_total_weight_volume(self):
        for record in self:
            record.shipped_weight = sum(product.product_id.weight * product.quantity for product in record.move_line_ids)
            record.shipped_volume = sum(product.product_id.volume * product.quantity for product in record.move_line_ids)

    
    
    
                