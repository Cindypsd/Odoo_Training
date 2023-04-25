from odoo import fields, models

class PropertyType(models.Model):
    _name = "property.type"
    _description = "This is a model that represents the different types of properties"

    name = fields.Char(required=True)
    property_ids = fields.One2many("property", "property_type_id")
