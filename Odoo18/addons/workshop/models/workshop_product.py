from odoo import models, fields, api


class Product(models.Model):
    # _inherit = "product.template"
    _name = "workshop.product"
    _description = "Product model"

    # == FIELDS == #

    name = fields.Char(string="Name")
    product_template_id = fields.Many2one(
        "product.template", string="Related Product", required=True
    )
    min_stock = fields.Integer(string="Minimum stock", default=0)
    max_stock = fields.Integer(string="Maximum stock", default=0)
    maintenance_ids = fields.Many2many(
        comodel_name="workshop.maintenance",
        string="Maintenances",
    )
