from odoo import models, fields, api


class Maintenance(models.Model):
    _name = 'workshop.maintenance'
    _description = 'Workshop Maintenance'
    
    name = fields.Char(string="Name", default='New')
    entry_date = fields.Datetime(string="Entry date")
    vehicle_id = fields.Many2one('workshop.vehicle', string="Vehicle", required=True)
    departure_date = fields.Datetime(string="Departure Date")
    responsible_mechanic_id = fields.Many2one('workshop.employee', string='Responsible mechanic')
    
    # ============ #
    # CRUD METHODS #
    # ============ #

    @api.model_create_multi
    def create(self, vals_list):

        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                
                # Get the customer_id and year
                base_code = 'MNT'
                year = fields.Date.today().year
                
                # Get the base sequence
                seq_code = f"maintenance.order.{base_code}.{year}"

                # Search if the sequence exist
                sequence = self.env['ir.sequence'].search([('code', '=', seq_code)], limit=1)
                if not sequence:
                    sequence = self.env['ir.sequence'].create({
                    'name': f"Maintenance {base_code} {year}",
                    'code': seq_code,
                    'prefix': f"{base_code}/{year}/",
                    'padding': 4,
                    'number_increment': 1,
                    'implementation': 'standard',
                    'use_date_range': False,
                })

                vals['name'] = sequence.next_by_id()

        return super(Maintenance, self).create(vals)