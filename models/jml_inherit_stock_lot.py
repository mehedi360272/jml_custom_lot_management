from odoo import models, fields, api


class StockLot(models.Model):
    _inherit = 'stock.lot'

    supplier_source_id = fields.Many2one(
        'jml.supplier.source',
        string='Supplier Source'
    )
    lock_unlock = fields.Boolean(string="Lock/Unlock", default=False)
    is_lock = fields.Boolean(string="Is Lock")

    @api.model
    def create(self, vals):
        if vals.get('product_id'):
            product = self.env['product.product'].browse(vals['product_id'])
            template = product.product_tmpl_id
            vals['is_lock'] = template.lock_product
        return super(StockLot, self).create(vals)
