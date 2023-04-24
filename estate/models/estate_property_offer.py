from odoo import fields, models


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
