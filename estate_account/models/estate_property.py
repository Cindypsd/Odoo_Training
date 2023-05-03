from odoo import models, Command

class EstateProperty(models.Model):
    _inherit = 'property'

    def action_sold(self):
        accepted_offer = self.offer_ids.find_accepted_offer()
        self.env['account.move'].create({
        'partner_id': accepted_offer.partner_id.id,
        'move_type': 'out_invoice',
        'journal_id': self.env["account.journal"].search([("type", "=", "sale")], limit=1).id,
        'invoice_line_ids': [
            Command.create(
                {"name": self.name,
                "quantity": 1,
                "price_unit": self.selling_price
            }),
            Command.create({
                'name': 'Administrative Fees',
                'quantity': 1,
                'price_unit': 100.00,
            }),
            Command.create({
                'name': 'Sales Commission',
                'quantity': 1,
                'price_unit': self.selling_price * 0.06,
            })
        ]

        })
        return super().action_sold()
