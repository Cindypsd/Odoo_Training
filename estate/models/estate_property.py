# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import fields, models

class EstateProperty(models.Model):
    _name = "property"
    _description = "This model provides a representation of a real estate"

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
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
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
    property_type_id = fields.Many2one("property.type")
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user.id,
    )

    buyer_id = fields.Many2one("res.partner", copy=False)
    tag_ids = fields.Many2many("property.tag")
    partner_id = fields.Many2one("res.partner")
    offer_ids = fields.One2many("property.offer", "property_id")


