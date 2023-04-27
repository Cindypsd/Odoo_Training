from odoo import api, fields, models

class PropertyType(models.Model):
    _name = "property.type"
    _description = "This is a model that represents the different types of properties"
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("property", "property_type_id")
    offer_ids = fields.One2many("property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'The name must be unique'),
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    def get_offers(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Offers",
            "view_mode": "tree",
            "res_model": "property.offer",
            "domain": [("property_type_id", "=", self.id)],
            "context": "{'create': False}",
        }





