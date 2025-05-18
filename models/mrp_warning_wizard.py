from odoo import models, fields, api, _


class MrpWarningWizard(models.TransientModel):
    _name = 'mrp.warning.wizard'
    _description = 'MRP Warning Wizard'

    warning_message = fields.Text(string='Warning Message', readonly=True)

    def action_confirm(self):
        # Get active production record from context
        production_id = self.env.context.get('active_id')
        production = self.env['mrp.production'].browse(production_id)

        # Call original button_mark_done to complete production
        production.button_mark_done_original()

        # Close the wizard
        return {'type': 'ir.actions.act_window_close'}


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def button_mark_done(self):
        warning_messages = []
        for production in self:
            for move in production.move_raw_ids.move_line_ids:
                if not move.product_id or not move.quantity or not move.location_id or not move.lot_id:
                    continue

                if move.lot_id.is_lock:
                    quant = self.env['stock.quant'].search([
                        ('product_id', '=', move.product_id.id),
                        ('location_id', '=', move.location_id.id),
                        ('lot_id', '=', move.lot_id.id)
                    ], limit=1)
                    lot_onhand_qty = quant.quantity if quant else 0.0

                    if move.quantity != lot_onhand_qty:
                        warning_messages.append(
                            f"Lot '{move.lot_id.name}' for product '{move.product_id.display_name}' has "
                            f"{lot_onhand_qty:.2f} quantity on-hand in '{move.location_id.display_name}', "
                            f"but you're trying to use {move.quantity}. You must match it exactly."
                        )
        if warning_messages:
            return {
                'name': _('Warning'),
                'type': 'ir.actions.act_window',
                'res_model': 'mrp.warning.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_warning_message': '\n'.join(warning_messages),
                    'active_id': self.id,
                },
            }

        # If no warnings, call original method to finish production
        return self.button_mark_done_original()

    def button_mark_done_original(self):
        # Call super to do actual mark done work
        return super(MrpProduction, self).button_mark_done()
