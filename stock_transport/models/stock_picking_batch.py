from odoo import fields, models, api

class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"
    
    dock_id = fields.Many2one("inventory.dock")
    vehicle_id = fields.Many2one("fleet.vehicle")
    category_id = fields.Many2one('fleet.vehicle.model.category', string="Vehicle Category")
    weight = fields.Float("Weight", compute="compute_weight", readonly=True, store=True)
    volume = fields.Float("Volume", compute="compute_volume", readonly=True, store=True)
    transfer = fields.Float("#Transfer", compute="compute_transfer", store=True)
    lines = fields.Float("#Lines", compute="compute_lines", store=True)
    date_deadline = fields.Date(string='Deadline', index=True, copy=False, default=fields.Date.context_today)
    date_start = fields.Date(string='Start date', index=True, copy=False, default=fields.Date.context_today)
    
    @api.depends("move_line_ids", "category_id")
    def compute_weight(self):
        w = 0
        for record in self:
            line = record.move_line_ids
            for product in line:
                w = w + product.product_id.weight * product.quantity
                
        if self.category_id.max_weight > 0:
            self.weight = w / self.category_id.max_weight
        else:
            self.weight = w
    
            
    @api.depends("move_line_ids", "category_id")
    def compute_volume(self):
        vol = 0
        for record in self:
            line = record.move_line_ids
            for product in line:
                vol = vol + product.product_id.volume * product.quantity
                
        if self.category_id.max_volume > 0:
            self.volume = vol / self.category_id.max_volume
        else:
            self.volume = vol
    
    
    @api.depends("picking_ids")
    def compute_transfer(self):
        for record in self:
            curr = len(record.picking_ids)
            record.transfer = curr
            
    @api.depends("move_line_ids")
    def compute_lines(self):
        for record in self:
            curr = len(record.move_line_ids)
            record.lines = curr

        
        
    # @api.depends("category_id.max_weight")
    # def _compute_weight_progress(self):
    #     for record in self:
    #         if record.category_id.max_weight:
    #             total_weight = sum(record.weights)
    #             weight_progress = total_weight / record.category_id.max_weight
    #             record.weight_progress = weight_progress
    #         else:
    #             record.weight_progress = 0.0
