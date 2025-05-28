from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    supplier_source_id = fields.Many2one('jml.supplier.source', string='Supplier Source',
                                         help="The supplier from whom the raw materials were sourced.")
    lot_note = fields.Html(string='Lot Note', help="Any important note regarding the lot or production batch.")

    def action_confirm(self):
        for production in self:
            if production.state not in ('confirmed', 'in_progress', 'done', 'cancel'):
                production.write({'state': 'confirmed'})
                production._has_workorders()
        return True

    # Overrides qty_producing onchange to skip execution if the related product is locked (lock_product=True), ensuring restricted quantity updates.
    @api.onchange('qty_producing', 'lot_producing_id')
    def _onchange_producing(self):
        if self.product_id and self.product_id.lock_product:
            return
        super()._onchange_producing()

    # ...........................
    def action_generate_serial(self):
        self.ensure_one()

        if not self.lot_producing_id:
            lot_prefix = self.product_id.product_tmpl_id.lot_prefix or ''
            lot_name = f"{lot_prefix}{self.env['ir.sequence'].next_by_code('stock.lot.serial')}"

            lot_vals = {
                'name': lot_name,
                'product_id': self.product_id.id,
                'company_id': self.company_id.id,
                # এখানে mrp.production থেকে supplier_source_id ও note কপি
                'supplier_source_id': self.supplier_source_id.id if self.supplier_source_id else False,
                'note': self.lot_note or '',
            }
            lot = self.env['stock.lot'].create(lot_vals)
            self.lot_producing_id = lot

        if self.product_id.tracking == 'serial':
            self._set_qty_producing(False)

        if self.picking_type_id.auto_print_generated_mrp_lot:
            return self._autoprint_generated_lot(self.lot_producing_id)
