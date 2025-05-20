from odoo import models, fields


class ProductProduct(models.Model):
    _inherit = 'product.product'


    tracking = fields.Selection(related='product_tmpl_id.tracking', store=True)
    lot_count_value = fields.Float(
        string="Lot On Hand",
        compute='_compute_lot_count_value'
    )

    def _compute_lot_count_value(self):
        for product in self:
            product.lot_count_value = product.product_tmpl_id.lot_count

    def action_view_lots(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Lots',
            'res_model': 'stock.lot',
            'view_mode': 'list,form',
            'domain': [
                ('product_id', '=', self.id),
                ('product_qty', '>', 0),
            ],
            'context': {'search_default_group_by_product_id': 1},
        }