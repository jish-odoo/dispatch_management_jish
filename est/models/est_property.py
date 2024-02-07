from odoo import models, fields

class EstateProperty(models.Model):
    _name = "est_model"
    _description = "Real Estate Property"

    name = fields.Char(string="Property Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Availability Date")
    expected_price = fields.Float(string="Expected Price",required=True)
    selling_price = fields.Float(string="Selling Price")
    bedrooms = fields.Integer(string="Number of Bedrooms")
    living_area = fields.Integer(string="Living Area (sq. ft.)")
    facades = fields.Integer(string="Number of Facades")
    garage = fields.Boolean(string="Has Garage")
    garden = fields.Boolean(string="Has Garden")
    garden_area = fields.Integer(string="Garden Area (sq. ft.)")
    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string="Garden Orientation",
    )
    
    
