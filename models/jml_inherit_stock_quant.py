from odoo import models, fields, api


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    # Computed field to store the related Supplier Source from the lot
    supplier_source_data = fields.Many2one(
        'jml.supplier.source',
        string="Supplier Source",
        compute="_compute_supplier_source_data",  # Value is computed from method below
        store=True  # Store in database so it's searchable and usable in group by
    )

    # Computed field to store the Note from the lot
    lot_note = fields.Html(
        string="Note",
        compute="_compute_supplier_source_data",  # Same compute method
        store=True  # Store in database
    )

    # Compute method triggered when lot_id, or lot's supplier_source_id or note changes
    @api.depends('lot_id', 'lot_id.supplier_source_id', 'lot_id.note')
    def _compute_supplier_source_data(self):
        for record in self:
            # Assign supplier source if available in lot
            record.supplier_source_data = (
                record.lot_id.supplier_source_id if record.lot_id else False
            )

            # Assign note from lot if available
            record.lot_note = (
                record.lot_id.note if record.lot_id else ''
            )

    # Override write method to force recompute if lot_id is changed manually
    def write(self, vals):
        res = super().write(vals)
        if 'lot_id' in vals:
            # Force recompute if lot_id is changed in write
            self._compute_supplier_source_data()
        return res
