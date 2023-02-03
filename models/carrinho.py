from odoo import models, fields, api, _


class InheritProduct(models.Model):
    _name = 'carrinho'

    product_id = fields.Many2one('product.product')

    cotacao_id = fields.Many2one('cotacao.wizard')

    vai_comprar = fields.Boolean(
        string="Sera comprado",
        default=True
    )

    etq_insuficiente = fields.Boolean(
        string="Atende a demanda?",
        help="Não atende ou atende "
             "parcialmente a demanda",
        default=False
    )

    quantidade_requisitada = fields.Integer(
        string="Quantidade requisitada",
        default=None
    )
