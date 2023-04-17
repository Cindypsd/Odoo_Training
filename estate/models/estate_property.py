# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import fields, models

class EstateProperty(models.Model):
    _name = "property"
    _description = "Test Model for Training"
   
    name = fields.Char(string = 'Name', required=True)
    description = fields.Text(string = 'Description')
    postcode = fields.Char(string = 'Postcode')
    date_availability = fields.Date(string = 'Availability Date', copy=False, default=datetime.now().date() + timedelta(days=30))
    expected_price = fields.Float(string = 'Expected Price', required=True)
    selling_price = fields.Float(string = 'Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer(string = 'Bedrooms', default=2)
    living_area = fields.Integer(string = 'Living Area (sqm)')
    facades = fields.Integer(string = 'Farcades')
    garage = fields.Boolean(string = 'Garage')
    garden = fields.Boolean(string = 'Garden')
    garden_area = fields.Integer(string = 'Garden Area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('North', 'North'),
            ('South', 'South'),
            ('East', 'East'),
            ('West', 'West')
        ],
    )
    state = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
    active = fields.Boolean(string='Active', default=True)
    property_type_id = fields.Many2one("property.type", string="Property Type")
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user.id,
    )

    
