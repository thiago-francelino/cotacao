from odoo import models, fields, api, _
from odoo.exceptions import UserError

class InheritOrderSale(models.Model):

    _inherit = 'sale.order'

    # todos_produtos = fields.Many2one(
    #     'carrinho',
    #     string="Todos produtos cotados",
    #     readonly=True
    # )

    todos_produtos = fields.Many2many(
        'carrinho',
        string="Todos produtos cotados",
        readonly=True,
        realtion="rel_sale_order_carrinho"
    )
