from odoo import fields, models


class PropertyTag(models.Model):
    _name = "property.tag"
    _description = "This is a model that represents tags that can be associated with different properties."

    name = fields.Char(required=True)
