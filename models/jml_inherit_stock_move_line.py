from odoo import models, fields, api
from odoo.exceptions import ValidationError


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    supplier_source_id = fields.Many2one("jml.supplier.source")


    @api.onchange('product_id', 'quantity', 'location_id', 'lot_id')
    def _onchange_quantity_vs_onhand(self):
        for move in self:
            if not move.product_id or not move.quantity or not move.location_id or not move.lot_id:
                continue

            # Check if the lot is locked
            if move.lot_id.is_lock:
                # Fetch on-hand quantity specific to the lot
                quant = self.env['stock.quant'].search([
                    ('product_id', '=', move.product_id.id),
                    ('location_id', '=', move.location_id.id),
                    ('lot_id', '=', move.lot_id.id)
                ], limit=1)

                lot_onhand_qty = quant.quantity if quant else 0.0

                if move.quantity > lot_onhand_qty:
                    return {
                        'warning': {
                            'title': 'Warning! Maximum Quantity Reached!',
                            'message': f"Demanded quantity ({move.quantity}) is greater than on-hand quantity ({lot_onhand_qty:.2f}) for lot '{move.lot_id.name}' of product '{move.product_id.display_name}'.",
                        }
                    }
                elif move.quantity < lot_onhand_qty:
                    return {
                        'warning': {
                            'title': 'Warning! Quantity Less Than On-Hand!',
                            'message': f"Demanded quantity ({move.quantity}) is less than on-hand quantity ({lot_onhand_qty:.2f}) for lot '{move.lot_id.name}' of product '{move.product_id.display_name}'.",
                        }
                    }
