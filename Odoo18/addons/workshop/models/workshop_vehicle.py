from odoo import models, fields

class Vehicle(models.Model):
    _name = 'workshop.vehicle'
    _description = 'Vehicle model'

    #=== FIELDS ===#
    
    plate = fields.Char(string = 'Plate')
    brand = fields.Char(string = 'Brand')
    model = fields.Char(string = 'Model')
    customer_id = fields.Many2one(
        'workshop.customer',
        string = 'Customer'
    )