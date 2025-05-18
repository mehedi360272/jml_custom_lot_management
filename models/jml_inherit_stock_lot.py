from odoo import models, fields, api

class StockLot(models.Model):
    _inherit = 'stock.lot'

    supplier_source_id = fields.Many2one(
        'jml.supplier.source',
        string='Supplier Source'
    )
    lock_unlock = fields.Boolean(string="Lock/Unlock", default=False)
    is_lock = fields.Boolean(string="Is Lock", default=True, required=True)


