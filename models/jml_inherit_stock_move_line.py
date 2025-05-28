from odoo import models, fields, api
from odoo.exceptions import ValidationError


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    # These fields will be auto-filled from the related Lot via the Quant
    supplier_source_id = fields.Many2one('jml.supplier.source', string='Source Location')
    note = fields.Html(string='Note')

    @api.onchange('quant_id')
    def _onchange_quant_id_get_supplier_and_note(self):
        """
        When the quant_id is changed on a stock move line,
        automatically pull the supplier_source_id and note from the associated Lot (via quant.lot_id)
        """
        for line in self:
            lot = line.quant_id.lot_id if line.quant_id else False
            if lot:
                # Set supplier source from the lot, if available
                if lot.supplier_source_id:
                    line.supplier_source_id = lot.supplier_source_id
                # Set note from the lot, if available
                if lot.note:
                    line.note = lot.note

    @api.model
    def create(self, vals):
        """
        When a stock.move.line record is created, pull supplier_source_id and note
        from the related lot through quant_id
        """
        res = super().create(vals)
        for line in res:
            lot = line.quant_id.lot_id if line.quant_id else False
            if lot:
                if lot.supplier_source_id:
                    line.supplier_source_id = lot.supplier_source_id
                if lot.note:
                    line.note = lot.note
        return res

    def write(self, vals):
        """
        When a stock.move.line is updated, also update the supplier_source_id and note
        from the associated lot if quant_id is involved
        """
        res = super().write(vals)
        for line in self:
            lot = line.quant_id.lot_id if line.quant_id else False
            if lot:
                if lot.supplier_source_id:
                    line.supplier_source_id = lot.supplier_source_id
                if lot.note:
                    line.note = lot.note
        return res

    @api.onchange('quant_id')
    def _onchange_quant_id_get_supplier_and_note(self):
        for line in self:
            lot = line.quant_id.lot_id if line.quant_id else False
            if lot:
                if lot.supplier_source_id:
                    line.supplier_source_id = lot.supplier_source_id
                if lot.note:
                    line.note = lot.note

            # Auto-set quantity from quant's available_quantity if product is locked
            if line.quant_id and line.quant_id.product_id.lock_product:
                line.quantity = line.quant_id.available_quantity

    # @api.onchange('product_id', 'quantity', 'location_id', 'lot_id')
    # def _onchange_quantity_vs_onhand(self):
    #     for move in self:
    #         if not move.product_id or not move.quantity or not move.location_id or not move.lot_id:
    #             continue
    #
    #         # Product lock check from product.template
    #         if move.product_id.product_tmpl_id.lock_product:
    #             quant = self.env['stock.quant'].search([
    #                 ('product_id', '=', move.product_id.id),
    #                 ('location_id', '=', move.location_id.id),
    #                 ('lot_id', '=', move.lot_id.id)
    #             ], limit=1)
    #
    #             lot_onhand_qty = quant.quantity if quant else 0.0
    #
    #             if move.quantity > lot_onhand_qty:
    #                 return {
    #                     'warning': {
    #                         'title': 'Warning! Maximum Quantity Reached!',
    #                         'message': f"Product '{move.product_id.display_name}' is locked. Demanded quantity ({move.quantity}) exceeds on-hand quantity ({lot_onhand_qty:.2f}) for lot '{move.lot_id.name}'.",
    #                     }
    #                 }
    #             elif move.quantity < lot_onhand_qty:
    #                 return {
    #                     'warning': {
    #                         'title': 'Warning! Quantity Less Than On-Hand!',
    #                         'message': f"Product '{move.product_id.display_name}' is locked. Demanded quantity ({move.quantity}) is less than on-hand quantity ({lot_onhand_qty:.2f}) for lot '{move.lot_id.name}'.",
    #                     }
    #                 }

    # ...............................................
    is_internal_transfer = fields.Boolean(
        string="Is Internal Transfer", compute="_compute_is_internal_transfer", store=True
    )

    @api.depends('picking_id.picking_type_id.code')
    def _compute_is_internal_transfer(self):
        for record in self:
            code = record.picking_id.picking_type_id.code if record.picking_id and record.picking_id.picking_type_id else ''
            record.is_internal_transfer = code == 'internal'

