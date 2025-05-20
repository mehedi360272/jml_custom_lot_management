from odoo import models, fields


class ProductProduct(models.Model):
    _inherit = 'product.product'

    lot_count_value = fields.Float(
        string="Lot On Hand",
        compute='_compute_lot_count_value'
    )

    def _compute_lot_count_value(self):
        for product in self:
            product.lot_count_value = product.product_tmpl_id.lot_count
