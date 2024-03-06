from odoo import fields, models, api

class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"
    
    dock_id = fields.Many2one("inventory.dock", string="Dock", create="True")
    vehicle_id = fields.Many2one("fleet.vehicle")
    category_id = fields.Many2one('fleet.vehicle.model.category', string="Vehicle Category")
    weight = fields.Float(compute="compute_weight_and_volume_progress", readonly=True, store=True)
    volume = fields.Float(compute="compute_weight_and_volume_progress", readonly=True, store=True)
    transfer = fields.Float("#Transfer", compute="compute_transfer_lines", store=True)
    lines = fields.Float("#Lines", compute="compute_transfer_lines", store=True)
    date_deadline = fields.Date(string='Deadline', index=True, copy=False, default=fields.Date.context_today)
    date_start = fields.Date(string='Start date', index=True, copy=False, default=fields.Date.context_today)
    
    shipped_volume = fields.Float(compute="compute_total_weight_volume")
    shipped_weight = fields.Float(compute="compute_total_weight_volume")
    
    @api.depends("move_line_ids")
    def compute_total_weight_volume(self):
        w = 0
        vol = 0
        for record in self:
            line = record.move_line_ids
            for product in line:
                w = w + product.product_id.weight * product.quantity
                vol = vol + product.product_id.volume * product.quantity
        self.shipped_weight = w
        self.shipped_volume = vol
    
    @api.depends("move_line_ids", "category_id")
    def compute_weight_and_volume_progress(self):
        total_weight = 0
        total_volume = 0
        for record in self:
            line = record.move_line_ids
            for product in line:
                total_weight += product.product_id.weight * product.quantity
                total_volume += product.product_id.volume * product.quantity
                
        if self.category_id.max_weight > 0:
            self.weight = total_weight / self.category_id.max_weight
        else:
            self.weight = total_weight

        if self.category_id.max_volume > 0:
            self.volume = total_volume / self.category_id.max_volume
        else:
            self.volume = total_volume

    
    
    @api.depends("picking_ids","move_line_ids")
    def compute_transfer_lines(self):
        for record in self:
            record.transfer = len(record.picking_ids)
            record.lines = len(record.move_line_ids)
            

            
