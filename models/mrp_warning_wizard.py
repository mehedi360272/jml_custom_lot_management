from odoo import models, fields, api, _


class MrpWarningWizardConfirmed(models.TransientModel):
    _name = 'mrp.warning.wizard.confirmed'
    _description = 'MRP Warning Wizard (Confirmed State)'

    warning_message = fields.Text(string='Warning Message', readonly=True)

    def action_confirm(self):
        production = self.env['mrp.production'].browse(self.env.context.get('active_id'))
        return production.with_context(bypass_warning=True).button_mark_done()


class MrpWarningWizardProgress(models.TransientModel):
    _name = 'mrp.warning.wizard.progress'
    _description = 'MRP Warning Wizard (Progress State)'

    warning_message = fields.Text(string='Warning Message', readonly=True)

    def action_confirm(self):
        production = self.env['mrp.production'].browse(self.env.context.get('active_id'))
        return production.with_context(bypass_warning=True).custom_backorder_action()


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def button_mark_done(self):
        if self.env.context.get('bypass_warning'):
            return super().button_mark_done()

        warning_messages = self._check_locked_products()

        if warning_messages:
            return {
                'name': _('Warning'),
                'type': 'ir.actions.act_window',
                'res_model': 'mrp.warning.wizard.confirmed',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_warning_message': '\n'.join(warning_messages),
                    'active_id': self.id,
                },
            }

        return super().button_mark_done()

    def custom_backorder_action(self):
        self.write({'state': 'progress'})
        return True

    def trigger_backorder_check(self):
        warning_messages = self._check_locked_products()

        if warning_messages:
            return {
                'name': _('Warning'),
                'type': 'ir.actions.act_window',
                'res_model': 'mrp.warning.wizard.progress',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_warning_message': '\n'.join(warning_messages),
                    'active_id': self.id,
                },
            }

        return self.custom_backorder_action()

    def _check_locked_products(self):
        messages = []

        for move in self.move_raw_ids:
            product = move.product_id
            total_quantity = sum(move_line.quantity for move_line in move.move_line_ids)

            # Expected qty based on qty_producing
            if not product.uom_id or not self.product_uom_id:
                continue

            expected_qty = self.product_uom_id._compute_quantity(self.qty_producing, product.uom_id)

            # Check lot-wise mismatch if locked
            if product.lock_product and move.lot_ids:
                for move_line in move.move_line_ids:
                    if not move_line.lot_id:
                        continue
                    quant = self.env['stock.quant'].search([
                        ('product_id', '=', product.id),
                        ('location_id', '=', move_line.location_id.id),
                        ('lot_id', '=', move_line.lot_id.id)
                    ], limit=1)
                    if quant and move_line.quantity > quant.quantity:
                        messages.append(
                            f"Product '{product.display_name}' is locked. "
                            f"Lot '{move_line.lot_id.name}' has {quant.quantity} in stock, "
                            f"but you're using {move_line.quantity}."
                        )

            # Check total consumption vs expected
            if abs(total_quantity - expected_qty) > 0.0001:
                messages.append(
                    f"Product '{product.display_name}' used {total_quantity} units, "
                    f"but expected for {self.qty_producing} finished qty is {expected_qty} units."
                )

        return messages
