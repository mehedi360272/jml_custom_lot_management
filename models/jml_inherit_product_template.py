from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'product.template'

    lot_prefix = fields.Char(string="Lot Prefix")

    avg_uom_calculation = fields.Selection(
        selection=[
            ('1', 'U1 / U2'),
            ('2', 'U2 / U1'),
        ],
        string="UOM Calculation",
        required=True
    )
    avg_weight = fields.Float(string="Average Weight")

    lock_product = fields.Boolean(string='Lock Product')