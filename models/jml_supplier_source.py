from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SupplierSource(models.Model):
    _name = 'jml.supplier.source'
    _description = 'Supplier Source'
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The supplier name already exist.')
    ]

    name = fields.Char(string="Name", required=True)

