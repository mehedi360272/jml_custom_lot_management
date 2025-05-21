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
