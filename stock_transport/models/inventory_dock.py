from odoo import models, fields

class InventoryDock(models.Model):
    _name = "inventory.dock"
    _description = "Docks for Inventory"
    
    name = fields.Char("Name")
    