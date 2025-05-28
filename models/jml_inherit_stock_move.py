from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class StockMove(models.Model):
    _inherit = 'stock.move'

    # copy supplier_source_id and note from the move line and save this data in lot
    def _action_done(self, cancel_backorder=False):
        res = super()._action_done(cancel_backorder=cancel_backorder)

        for move in self:
            for move_line in move.move_line_ids:
                lot = move_line.lot_id
                if lot and move_line.supplier_source_id:
                    lot.supplier_source_id = move_line.supplier_source_id
                if lot and move_line.note:
                    lot.note = move_line.note
        return res

    def _action_assign(self):
        unlocked_moves = self.filtered(lambda m: not m.product_id.lock_product)
        locked_moves = self.filtered(lambda m: m.product_id.lock_product)

        for move in locked_moves:
            move.state = 'confirmed'

        return super(StockMove, unlocked_moves)._action_assign()



    # ...................................
    # @api.constrains('product_uom_qty')
    # def _check_product_uom_qty_vs_move_lines(self):
    #     for move in self:
    #         if move.product_id.lock_product:
    #             total_move_line_qty = sum(move.move_line_ids.mapped('quantity'))
    #             if total_move_line_qty > move.product_uom_qty:
    #                 raise ValidationError(
    #                     "Product %s is locked. The total quantity in move lines (%s) cannot be less than the move quantity (%s)." % (
    #                         move.product_id.display_name,
    #                         total_move_line_qty,
    #                         move.product_uom_qty
    #                     )
    #                 )
