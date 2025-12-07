from odoo import models, fields, api


class Maintenance(models.Model):
    _name = "workshop.maintenance"
    _description = "Workshop Maintenance"

    # == FIELDS == #

    name = fields.Char(string="Name", default="New")
    date_request = fields.Date(string="Date request")
    date_start = fields.Datetime(string="Date Start")
    date_end = fields.Datetime(string="Date end")
    date_delivery = fields.Datetime(string="Date delivery")
    customer_id = fields.Many2one(
        "workshop.customer", string="Customer", required=True
    )
    vehicle_id = fields.Many2one(
        "workshop.vehicle", string="Vehicle", required=True
    )
    product_ids = fields.Many2many(
        comodel_name="workshop.product",
        string="Products",
    )
    mechanic_id = fields.Many2one(
        comodel_name="workshop.employee", string="Mechanic", required=True
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("in_progress", "In progress"),
            ("quality_check", "Quality Check"),
            ("ready", "Ready for delivery"),
            ("delivered", "Delivered"),
            ("invoiced", "Invoiced"),
            ("cancelled", "Cancelled"),
        ],
        string="State",
        default="draft",
        tracking=True,
    )
    priority = fields.Selection(
        [("low", "Low"), ("normal", "Normal"), ("high", "High"), ("urgent", "Urgent")],
        string="Priority",
        default="normal",
    )
    problem_description = fields.Text(string="Problems description", required=True)
    diagnosis = fields.Text(string="Diagnosis")
    internal_notes = fields.Text(string="Internal notes")
    customer_notes = fields.Text(string="Customer notes")
    km_at_entry = fields.Integer(string="KM at entry")
    km_at_exit = fields.Integer(string="KM at exit")
    line_ids = fields.One2many(
        "workshop.maintenance.line", "maintenance_id", string="Maintenance lines"
    )
    total_hours = fields.Float(
        string="Total hours", compute="_compute_totals", store=True
    )
    total_parts = fields.Float(
        string="Total spare parts", compute="_compute_totals", store=True
    )
    total_amount = fields.Float(
        string="Total amount", compute="_compute_totals", store=True
    )

    invoice_id = fields.Many2one("account.move", string="Invoice", readonly=True)
    invoiced_amount = fields.Float(
        string="Invoice amount", related="invoice_id.amount_total"
    )

    # == CRUD METHODS == #

    @api.model_create_multi
    def create(self, vals_list):

        for vals in vals_list:
            if vals.get("name", "New") == "New":

                # Get the customer_id and year
                base_code = "MNT"
                year = fields.Date.today().year

                # Get the base sequence
                seq_code = f"maintenance.order.{base_code}.{year}"

                # Search if the sequence exist
                sequence = self.env["ir.sequence"].search(
                    [("code", "=", seq_code)], limit=1
                )
                if not sequence:
                    sequence = self.env["ir.sequence"].create(
                        {
                            "name": f"Maintenance {base_code} {year}",
                            "code": seq_code,
                            "prefix": f"{base_code}/{year}/",
                            "padding": 4,
                            "number_increment": 1,
                            "implementation": "standard",
                            "use_date_range": False,
                        }
                    )

                vals["name"] = sequence.next_by_code(seq_code)

        return super(Maintenance, self).create(vals)

    # Completar método _compute_totals:
    @api.depends('line_ids.price_subtotal', 'line_ids.duration')
    def _compute_totals(self):
        for record in self:
            record.total_hours = sum(record.line_ids.mapped('duration'))
            record.total_parts = sum(record.line_ids.filtered(lambda l: l.product_type == 'product').mapped('price_subtotal'))
            record.total_amount = sum(record.line_ids.mapped('price_subtotal'))