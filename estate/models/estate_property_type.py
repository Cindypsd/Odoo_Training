from odoo import fields, models

class PropertyType(models.Model):
    _name = "property.type"
    _description = "Property type model"

   
    name = fields.Char(string = 'Name', required=True)
    property_ids = fields.One2many("property", "property_type_id", "Properties")