from odoo import models, fields, api

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if 'product_id' in res:
            product = self.env['product.product'].browse(res['product_id'])
            if product and product.tracking != 'none':
                prefix = product.product_tmpl_id.lot_prefix or ''
                seq = self.env['ir.sequence'].next_by_code('auto.lot.number')
                if seq:
                    res['lot_name'] = f"{prefix}{seq}"
        return res

    @api.model
    def create(self, vals):
        if not vals.get('lot_name') and vals.get('product_id'):
            product = self.env['product.product'].browse(vals['product_id'])
            if product and product.tracking != 'none':
                prefix = product.product_tmpl_id.lot_prefix or ''
                seq = self.env['ir.sequence'].next_by_code('auto.lot.number')
                if seq:
                    vals['lot_name'] = f"{prefix}{seq}"
        return super().create(vals)
