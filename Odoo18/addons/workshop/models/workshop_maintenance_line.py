from odoo import models, fields, api


class WorkshopMaintenanceLine(models.Model):
    _name = "workshop.maintenance.line"
    _description = "Maintenances lines orders"

    maintenance_id = fields.Many2one(
        "workshop.maintenance", string="Maintenance", ondelete="cascade"
    )
    product_id = fields.Many2one(
        "product.product", string="Product", required=True
    )
    name = fields.Char(string="Name", required=True)
    quantity = fields.Float(string="Quantity", default=1.0)
    unit_price = fields.Float(string="Unit price")
    price_subtotal = fields.Float(
        string="Subtotal", compute="_compute_subtotal", store=True
    )

    product_type = fields.Selection(related="product_id.detailed_type", string="Type")
    duration = fields.Float(
        string="Duration", help="To services, duration in hours"
    )

    @api.depends("quantity", "unit_price")
    def _compute_subtotal(self):
        for line in self:
            line.price_subtotal = line.quantity * line.unit_price
