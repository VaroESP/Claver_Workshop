from odoo import models, fields, api
from odoo.tools import file_open

import base64


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
    last_maintenance = fields.Datetime(string="Last maintenance")
    next_maintenance = fields.Datetime(string="Next maintenance")
    vehicle_category = fields.Selection(
        [("car", "Car"), ("motorcycle", "Motorcycle"), ("truck", "Truck")]
    )
    maintenance_ids = fields.One2many(
        "workshop.maintenance", "vehicle_id", string="Maintenances"
    )
    avatar_128 = fields.Image(
        string="avatar 128",
        max_width=128,
        max_height=128,
        store=True,
        default=lambda self: self._get_default_avatar(),
    )

    # ================ #
    # COMPUTED METOHDS #
    # ================ #

    @api.depends("brand", "model")
    def _compute_name_vehicle(self):
        for record in self:
            brand_upper = str(record.brand or "").upper()
            model_upper = str(record.model or "").upper()
            parts = [brand_upper, model_upper]
            record.name = " ".join(filter(None, parts)) or False

    # =============== #
    # HELPERS METHODS #
    # =============== #

    @api.model
    def _get_default_avatar(self):
        try:
            with file_open("workshop/static/src/img/car_default.png", "rb") as f:
                return base64.b64encode(f.read())
        except Exception:
            return False

    # ============== #
    # ACTION METHODS #
    # ============== #

    def action_vehicle(self):
        return {
            "name": "Maintenances",
            "type": "ir.actions.act_window",
            "res_model": "workshop.maintenance",
            "view_mode": "list,form",
            "domain": [("vehicle_id", "=", self.id)],
            "target": "current",
        }
