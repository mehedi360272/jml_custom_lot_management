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


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    supplier_source_data = fields.Many2one(
        'jml.supplier.source',
        string="Supplier Source",
        compute="_compute_supplier_source_data",
        store=True
    )

    note = fields.Char(
        string="Note",
        compute="_compute_supplier_source_data",
        store=True
    )

    @api.depends('lot_id')
    def _compute_supplier_source_data(self):
        for record in self:
            record.supplier_source_data = (
                record.lot_id.supplier_source_id
                if record.lot_id and record.lot_id.supplier_source_id
                else False
            )
            record.note = (
                record.lot_id.note
                if record.lot_id and record.lot_id.note
                else ''
            )
