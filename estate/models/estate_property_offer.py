from datetime import timedelta
from odoo import api,fields, models, exceptions


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
    buyer_id = fields.Many2one("res.partner")
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("property", required=True)
    validity = fields.Integer(compute="_compute_validity", inverse="_inverse_validity", default = 7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.validity:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                record.validity = abs((record.date_deadline - fields.Date.today()).days)

    @api.depends("date_deadline")
    def _compute_validity(self):
        for record in self:
            record.validity = abs((record.date_deadline - fields.Date.today()).days) if record.date_deadline else 7

    def _inverse_validity(self):
        for record in self:
            record.date_deadline = fields.Date.today() + timedelta(days=(record.validity))

    def action_confirm(self):
        accepted_offer = self.property_id.offer_ids.filtered(lambda o : o.status == 'accepted')
        if accepted_offer:
            raise exceptions.UserError("More than one offer cannot be accepted")
        if self.property_id.expected_price and self.price < self.property_id.expected_price * 0.9:
            raise exceptions.UserError("The selling price must be at least 90% of the expected price! You must reduce the expected price if you want to accept this offer'")
        self.status = "accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.buyer_id

    def action_deny(self):
        for record in self:
            record.status = "refused"

    _sql_constraints = [
        (
            "check_price",
            "CHECK(price > 0)",
            "Offer price must be strictly positive",
        )
    ]
