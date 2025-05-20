from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        if self.picking_type_id.code == 'internal':
            warning_messages = self._check_locked_lots()
            if warning_messages:
                raise ValidationError("\n".join(warning_messages))

        return super().button_validate()

    def _check_locked_lots(self):
        messages = []
        for move_line in self.move_line_ids:
            if move_line.lot_id and move_line.lot_id.is_lock:
                quant = self.env['stock.quant'].search([
                    ('product_id', '=', move_line.product_id.id),
                    ('location_id', '=', move_line.location_id.id),
                    ('lot_id', '=', move_line.lot_id.id)
                ], limit=1)
                if quant and move_line.quantity != quant.quantity:
                    messages.append(_(
                        "Lot '%s' for product '%s' is locked. "
                        "Available quantity: %s, but you're transferring: %s."
                    ) % (
                                        move_line.lot_id.name,
                                        move_line.product_id.display_name,
                                        quant.quantity,
                                        move_line.quantity
                                    ))
        return messages
