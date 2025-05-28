from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        # Only validate for internal transfers
        if self.picking_type_id.code == 'internal':
            warning_messages = self._check_locked_products()
            if warning_messages:
                # Raise error if any locked products exceed planned quantity
                raise ValidationError("\n".join(warning_messages))
        return super().button_validate()

    def _check_locked_products(self):
        messages = []
        for move in self.move_ids:
            if move.product_id.lock_product:
                planned_qty = move.product_uom_qty
                total_done_qty = sum(
                    move.move_line_ids.filtered(lambda l: l.product_id == move.product_id).mapped('quantity'))
                if total_done_qty > planned_qty:
                    messages.append(_(
                        "Product '%s' is locked. "
                        "Demand quantity: %s, but you're transferring total: %s."
                    ) % (
                                        move.product_id.display_name,
                                        planned_qty,
                                        total_done_qty
                                    ))
        return messages
