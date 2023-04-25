from datetime import timedelta
from odoo import api,fields, models


class PropertyOffer(models.Model):
    _name = "property.offer"
    _description = "This model represents an offer made by a buyer for a property. "

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused")
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("property", required=True)
    validity = fields.Integer(compute="_compute_validity", inverse="_inverse_validity", default = 7)
    date_deadline = fields.Datetime()

    @api.depends("date_deadline")
    def _compute_validity(self):
        for record in self:
            record.validity = abs((record.date_deadline - fields.Datetime.now()).days) if record.date_deadline else 7

    def _inverse_validity(self):
        for record in self:
            record.date_deadline = fields.Datetime.now() + timedelta(days=(record.validity))

