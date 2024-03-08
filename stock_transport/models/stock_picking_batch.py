from odoo import fields, models, api

class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"
    
    dock_id = fields.Many2one("inventory.dock", string="Dock", create="True")
    vehicle_id = fields.Many2one("fleet.vehicle")
    category_id = fields.Many2one('fleet.vehicle.model.category', string="Vehicle Category")
    weight = fields.Float(compute="_compute_weight_and_volume_progress", readonly=True, store=True)
    volume = fields.Float(compute="_compute_weight_and_volume_progress", readonly=True, store=True)
    transfer = fields.Float("#Transfer", compute="compute_transfer_lines", store=True)
    lines = fields.Float("#Lines", compute="compute_transfer_lines", store=True)
    date_deadline = fields.Date(string='Deadline', index=True, copy=False, default=fields.Date.context_today)
    date_start = fields.Date(string='Start date', index=True, copy=False, default=fields.Date.context_today)
    display_name_gantt = fields.Char(compute='_compute_display_name_gantt', string='Gantt Display Name', store=False)
    
    shipped_volume = fields.Float(compute="compute_total_weight_volume")
    shipped_weight = fields.Float(compute="compute_total_weight_volume")
    
    
    @api.depends("move_line_ids")
    def compute_total_weight_volume(self):
        for record in self:
            record.shipped_weight = sum(product.product_id.weight * product.quantity for product in record.move_line_ids)
            record.shipped_volume = sum(product.product_id.volume * product.quantity for product in record.move_line_ids)
            
    
    @api.depends("move_line_ids", "category_id")
    def _compute_weight_and_volume_progress(self):
        for record in self:
            total_weight = sum(product.product_id.weight * product.quantity for product in record.move_line_ids)
            total_volume = sum(product.product_id.volume * product.quantity for product in record.move_line_ids)
            
            max_weight = record.category_id.max_weight or 1 
            max_volume = record.category_id.max_volume or 1  
            
            record.weight = total_weight / max_weight
            record.volume = total_volume / max_volume
            
    
    @api.depends("picking_ids","move_line_ids")
    def compute_transfer_lines(self):
        for record in self:
            record.transfer = len(record.picking_ids)
            record.lines = len(record.move_line_ids)
            
            
        
    @api.depends('weight', 'volume', 'name')
    def _compute_display_name_gantt(self):
        for record in self:
            if self.env.context.get('gantt_view'):
                record.display_name_gantt = f"{record.name} {record.weight}kg, {record.volume}m3"
            else:
                record.display_name_gantt = record.name

                    

            
