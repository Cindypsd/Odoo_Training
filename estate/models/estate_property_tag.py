from odoo import fields, models


class PropertyTag(models.Model):
    _name = "property.tag"
    _description = """
    This is a model that represents tags that can be associated with different properties.This model can be used in conjunction with the "property" model, as it allows users to add descriptive tags to each property record.
    """

    name = fields.Char(required=True)
