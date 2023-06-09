from odoo import fields, models


class PropertyTag(models.Model):
    _name = "property.tag"
    _description = "This is a model that represents tags that can be associated with different properties."
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'The name must be unique'),
    ]
