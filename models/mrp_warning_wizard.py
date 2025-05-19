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

        # Example validation logic
        warning_messages = self._check_locked_lots()

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
        # তোমার নিজের ব্যাকঅর্ডার লজিক
        self.write({'state': 'progress'})
        return True

    def trigger_backorder_check(self):
        warning_messages = self._check_locked_lots()

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

    def _check_locked_lots(self):
        messages = []
        for move in self.move_raw_ids.move_line_ids:
            if move.lot_id and move.lot_id.is_lock:
                quant = self.env['stock.quant'].search([
                    ('product_id', '=', move.product_id.id),
                    ('location_id', '=', move.location_id.id),
                    ('lot_id', '=', move.lot_id.id)
                ], limit=1)
                if quant and move.quantity != quant.quantity:
                    messages.append(
                        f"Lot '{move.lot_id.name}' for product '{move.product_id.display_name}' has "
                        f"{quant.quantity} in stock, but you're using {move.quantity}."
                    )
        return messages