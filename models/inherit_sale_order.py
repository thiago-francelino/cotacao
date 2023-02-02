from odoo import models, fields, api, _
from odoo.exceptions import UserError

class InheritPreCompra(models.Model):


    _inherit = 'sale.order'
    _name = 'sale.order'
    # _inherit = 'sale'
    # _inherit = 'sale.order.template'

    todos_produtos = fields.Many2many('product.product', string="Todos produtos cotados", readonly=True)
