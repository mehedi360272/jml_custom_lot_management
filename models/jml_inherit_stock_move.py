from odoo import models, fields


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