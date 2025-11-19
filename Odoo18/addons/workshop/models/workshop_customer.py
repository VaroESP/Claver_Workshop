from odoo import models, fields

class Customer(models.Model):
    _name = 'workshop.customer'
    _description = 'Customer model'
    _inherits = {'res.partner': 'partner_id'}

    #=== FIELDS ===#
    
    partner_id = fields.Many2one(
        'res.partner',
        string = 'Customer',
        required = True,
        ondelete = 'cascade'
    )
    street = fields.Char(string = 'Street')
    postal_code = fields.Char(string = 'Postal Code')
    phone = fields.Char(string = "Phone")
    vehicle_ids = fields.One2many(
        'workshop.vehicle',
        'customer_id',
        string = "Customer's Vehicles"
    )
