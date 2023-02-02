from odoo import models, fields, api, _


class InheritProduct(models.Model):
    _name = 'carrinho'
    _inherits = {
        'product.product': 'product_id',
    }

    product_id = fields.Many2one('product.product')

    vai_comprar = fields.Boolean(
        string="Sera comprado"
    )

    de_interesse = fields.Boolean(
        string="Item de interesse"
    )

    alt_flt_estoque = fields.Boolean(
        string="Alternativa a falta de estoque",
        help="É uma alternativa a falta de estoque "
             "ou cliente apresentou interesse alem "
             "do produto no qual ligou sobre"
    )

    etq_insuficiente = fields.Boolean(
        string="Estoque atende a demanda",
        help="Não atende ou atende "
             "parcialmente a demanda"
    )

    quantidade_requisitada = fields.Integer(
        string="Quantidade requisitada",
        default=None
    )
