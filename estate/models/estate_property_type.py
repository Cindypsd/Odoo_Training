from odoo import fields, models

class PropertyType(models.Model):
    _name = "property.type"
    _description = """
    This is a model that represents different types of properties, with the name of each property type as the primary field. The model is designed to be used in conjunction with the "property" model, as it has a one-to-many relationship with "property" to link each property with its respective property type.
    """


    name = fields.Char(required=True)
    property_ids = fields.One2many("property", "property_type_id", "Properties")
