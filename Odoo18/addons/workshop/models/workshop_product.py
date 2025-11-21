from odoo import models, fields


class Product(models.Model):
    _name = "workshop.product"
    _description = "Product model"

    # ====== #
    # FIELDS #
    # ====== #

    name = fields.Char(string="Name")
    product_template_id = fields.Many2one(
        'product.template', 
        string="Related Product",
        required=True
    )