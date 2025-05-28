from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.template'

    lot_prefix = fields.Char(string="Lot Prefix", store=True)

    avg_uom_calculation = fields.Selection(
        selection=[
            ('1', 'U1 / U2'),
            ('2', 'U2 / U1'),
        ],
        string="UOM Calculation", )
    avg_weight = fields.Float(string="Average Weight")

    lock_product = fields.Boolean(string='Lock Product')

    lot_count = fields.Float(
        string='Lot On Hand',
        compute='_compute_lot_count'
    )

    @api.depends('product_variant_ids')
    def _compute_lot_count(self):
        for template in self:
            products = template.product_variant_ids
            lots = self.env['stock.lot'].search([
                ('product_id', 'in', products.ids),
                ('product_qty', '>', 0)
            ])
            template.lot_count = len(lots)

    def action_view_lots(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Lots',
            'res_model': 'stock.lot',
            'view_mode': 'list,form',
            'domain': [
                ('product_id', 'in', self.product_variant_ids.ids),
                ('product_qty', '>', 0),
            ],
            'context': {'search_default_group_by_product_id': 1},
        }
