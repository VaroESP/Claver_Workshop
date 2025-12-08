from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Product(models.Model):
    _inherit = "product.template"
    _description = "Product model"

    # == FIELDS == #

    is_workshop_product = fields.Boolean(string="Workshop product", default=True)
    min_stock = fields.Integer(string="Minimum stock", default=0)
    max_stock = fields.Integer(string="Maximum stock", default=0)
    maintenance_ids = fields.Many2many(
        comodel_name="workshop.maintenance",
        string="Maintenances",
    )
    
    # Campos computados
    stock_status = fields.Selection(
        [
            ('sufficient', 'Sufficient'),
            ('low', 'Low Stock'),
            ('out', 'Out of Stock'),
            ('excess', 'Excess Stock'),
            ('unknown', 'Unknown')
        ],
        string="Stock Status",
        compute="_compute_stock_status",
        store=False  # Cambiado a store=False
    )

    # == CONSTRAINTS == #
    
    @api.constrains("min_stock", "max_stock")
    def _check_stock_limits(self):
        for record in self:
            if record.min_stock > record.max_stock:
                raise ValidationError(
                    "Minimum stock cannot be greater than maximum stock!"
                )
            if record.min_stock < 0 or record.max_stock < 0:
                raise ValidationError(
                    "Stock limits cannot be negative!"
                )

    # == COMPUTE METHODS == #
    
    def _compute_stock_status(self):
        """Calcular estado del stock basado en variantes"""
        for record in self:
            variants = record.product_variant_ids
            if not variants:
                record.stock_status = 'unknown'
                continue
                
            total_qty = sum(variant.qty_available for variant in variants)
            
            if total_qty <= 0:
                record.stock_status = 'out'
            elif record.min_stock > 0 and total_qty < record.min_stock:
                record.stock_status = 'low'
            elif record.max_stock > 0 and total_qty > record.max_stock:
                record.stock_status = 'excess'
            else:
                record.stock_status = 'sufficient'

    # == ACTION METHODS == #

    def action_view_maintenances(self):
        return {
            'name': 'Maintenances using this product',
            'type': 'ir.actions.act_window',
            'res_model': 'workshop.maintenance',
            'view_mode': 'tree,form',
            'domain': [('product_ids', 'in', self.product_variant_ids.ids)],
            'context': {},
        }