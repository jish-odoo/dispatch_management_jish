from odoo import fields, models, api

class StockPicking(models.Model):
    _inherit = "stock.picking"

    shipped_volume = fields.Float(compute="compute_volume")
    shipped_weight = fields.Float(compute="compute_weight")
    
    
    @api.depends("move_line_ids")
    def compute_weight(self):
        w = 0
        for record in self:
            line = record.move_line_ids
            for product in line:
                w = w + product.product_id.weight * product.quantity
        self.shipped_weight = w

    @api.depends("move_line_ids")
    def compute_volume(self):
        vol = 0
        for record in self:
            line = record.move_line_ids
            for product in line:
                vol = vol + product.product_id.volume * product.quantity
        self.shipped_volume = vol