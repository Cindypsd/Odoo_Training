# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import api,fields, models, tools, exceptions

class EstateProperty(models.Model):
    _name = "property"
    _description = "This model provides a representation of a real estate"
    _order= "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=datetime.now().date() + timedelta(days=30))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
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
    total_area = fields.Float(compute="_compute_total_area", string="Total Area (sqm)")
    best_offer = fields.Float(compute="_compute_best_price")
    sequence = fields.Integer(default=1)


    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                offer_prices = record.offer_ids.mapped("price")
                record.best_offer = max(offer_prices)
            else:
                record.best_offer = 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False


    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                raise exceptions.UserError("Canceled property cannot be sold")
            elif record.state == "sold":
                raise exceptions.UserError("Property is already sold")
            record.state = "sold"


    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise exceptions.UserError("Sold property cannot be canceled")
            elif record.state == "canceled":
                raise exceptions.UserError("Property is already canceled")
            record.state = "canceled"


    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                offer_prices = record.offer_ids.mapped("price")
                record.best_offer = max(offer_prices)
            else:
                record.best_offer = 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "Expected price must be strictly positive",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price > 0)",
            "Selling price must be strictly positive",
        )
    ]

    @api.ondelete(at_uninstall=False)
    def unlink_if_new_or_cancelled(self):
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise exceptions.UserError("Property can only be deleted if it's in 'New' or 'Canceled' state.")
