# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import fields, models

class EstateProperty(models.Model):
    _name = "property"
    _description = """
    This model provides a representation of a real estate property, including important fields such as the property name, description, postcode, date availability, expected price, selling price, number of bedrooms, living area, number of facades, and other features such as garage and garden.

    This model also includes fields to track the property's status, such as whether it is new, has an offer, has been accepted, sold, or canceled. It also includes a field to identify the salesperson responsible for selling the property and a field to track any potential buyers.
    """

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=datetime.now().date() + timedelta(days=30))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string = 'Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
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
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one("property.type", string="Property Type")
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user.id,
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("property.tag", string="Tags")
    partner_id = fields.Many2one("res.partner")
    offer_ids = fields.One2many("property.offer", "property_id")


