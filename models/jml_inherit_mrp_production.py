from odoo import models, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def action_confirm(self):
        for production in self:
            if production.state not in ('confirmed', 'in_progress', 'done', 'cancel'):
                production.write({'state': 'confirmed'})
                production._has_workorders()
        return True

    # def button_mark_done(self):
    #     for production in self:
    #         for move in production.move_raw_ids.move_line_ids:
    #             if not move.product_id or not move.quantity or not move.location_id or not move.lot_id:
    #                 continue
    #
    #             if move.lot_id.is_lock:
    #                 quant = self.env['stock.quant'].search([
    #                     ('product_id', '=', move.product_id.id),
    #                     ('location_id', '=', move.location_id.id),
    #                     ('lot_id', '=', move.lot_id.id)
    #                 ], limit=1)
    #
    #                 lot_onhand_qty = quant.quantity if quant else 0.0
    #
    #                 if move.quantity != lot_onhand_qty:
    #                     raise ValidationError(
    #                         f"[MRP] Locked lot '{move.lot_id.name}' for product '{move.product_id.display_name}' has "
    #                         f"{lot_onhand_qty:.2f} quantity on-hand in '{move.location_id.display_name}', "
    #                         f"but you're trying to use {move.quantity}. You must match it exactly."
    #                     )
    #
    #     return super(MrpProduction, self).button_mark_done()
