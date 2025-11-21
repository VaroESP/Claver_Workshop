from odoo import models, fields, api
from odoo.tools import file_open
from odoo.exceptions import ValidationError

import base64


class Employee(models.Model):
    _name = "workshop.employee"
    _description = "Employee model"

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

    def _is_user(self):
        pass

    def _create_user_from_student(self):
        self.ensure_one()
        if self.user_id:
            return self.user_id

        if not self.email:
            return False

        try:
            existing_user = self.env["res.users"].search(
                [("login", "=", self.email)], limit=1
            )

            if existing_user:
                self.user_id = existing_user.id
                return existing_user

            partner = self.env["res.partner"].search(
                [("email", "=", self.email)], limit=1
            )
            if not partner:
                partner = self.env["res.partner"].create(
                    {
                        "name": self.name,
                        "email": self.email,
                        "type": "contact",
                        "is_company": False,
                    }
                )

            user_vals = {
                "name": self.name,
                "login": self.email,
                "email": self.email,
                "partner_id": partner.id,
                "groups_id": [
                    (
                        6,
                        0,
                        [
                            self.env.ref("base.group_employee").id,
                        ],
                    )
                ],
                "active": True,
                "company_id": self.env.company.id,
                "company_ids": [(6, 0, [self.env.company.id])],
            }

            user = (
                self.env["res.users"]
                .with_context(no_reset_password=False)
                .create(user_vals)
            )
            self.user_id = user.id
            return user

        except Exception as e:
            raise ValidationError("No se pudo crear el usuario: %s" % str(e))

    @api.model
    def _get_default_avatar(self):
        try:
            with file_open("university/static/src/img/student_default.png", "rb") as f:
                return base64.b64encode(f.read())
        except Exception:
            return False

    # ============ #
    # CRUD METHODS #
    # ============ #

    @api.model_create_multi
    def create(self, vals_list):
        employees = super(Employee, self).create(vals_list)
        for student in employees:
            student._create_user_from_student()
        return employees
