from odoo import models, fields, api
from odoo.tools import file_open

import base64


class Customer(models.Model):
    _name = "workshop.customer"
    _description = "Customer model"

    # ====== #
    # FIELDS #
    # ====== #

    name = fields.Char(string="Name", required=True)
    street = fields.Char(string="Street")
    postal_code = fields.Char(string="Postal Code")
    city = fields.Char(string="City")
    state_id = fields.Many2one(
        "res.country.state",
        string="State",
        ondelete="restrict",
        domain="[('country_id', '=?', country_id)]",
        store=True,
    )
    country_id = fields.Many2one(
        "res.country", string="Country", ondelete="restrict", store=True
    )
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    avatar_128 = fields.Image(
        string="avatar 128",
        max_width=128,
        max_height=128,
        store=True,
        default=lambda self: self._get_default_avatar(),
    )
    vehicle_ids = fields.One2many(
        "workshop.vehicle", "customer_id", string="Customer's Vehicles"
    )

    # ================ #
    # ONCHANGE METHODS #
    # ================ #

    @api.onchange("state_id")
    def _onchange_state(self):
        if self.state_id:
            self.country_id = self.state_id.country_id
        else:
            self.country_id = False

    # =============== #
    # HELPERS METHODS #
    # =============== #

    @api.model
    def _get_default_avatar(self):
        try:
            with file_open("workshop/static/src/img/user_default.png", "rb") as f:
                return base64.b64encode(f.read())
        except Exception:
            return False
