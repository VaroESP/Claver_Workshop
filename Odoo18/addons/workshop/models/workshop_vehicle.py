from odoo import models, fields, api


class Vehicle(models.Model):
    _name = "workshop.vehicle"
    _description = "Vehicle model"

    # ====== #
    # FIELDS #
    # ====== #

    name = fields.Char(string="Vehicle", compute="_compute_name_vehicle", store=True)
    plate = fields.Char(string="Plate")
    brand = fields.Char(string="Brand")
    model = fields.Char(string="Model")
    customer_id = fields.Many2one("workshop.customer", string="Customer")
    vehicle_category = fields.Selection([("car", "Car"), ("motorcycle", "Motorcycle"), ("truck", "Truck")])
    mantinance_ids = fields.One2Many('workshop.maintenance', 'vehicle_id', string="Maintenances")

    # ================ #
    # COMPUTED METOHDS #
    # ================ #

    @api.depends("brand", "model")
    def _compute_name_vehicle(self):
        for record in self:
            parts = [record.brand, record.model]
            record.name = " ".join(filter(None, parts)) or False
