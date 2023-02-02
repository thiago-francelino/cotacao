from odoo import models, fields, api, _
from odoo.exceptions import UserError

class InheritPreCompra(models.Model):


    _inherit = 'product.product'

    vai_comprar = fields.Boolean(
        string="Sera comprado"
    )

    de_interesse = fields.Boolean(
        string="Item de interesse"
    )

    alt_flt_estoque = fields.Boolean(
        string="Alt flt desejado",
        help="É uma alternativa a falta de estoque "
             "ou cliente apresentou interesse alem "
             "do produto no qual ligou sobre"
    )

    alt_flt_variante = fields.Boolean(
        string="Alt flt variante",
        help="É uma alternativa a falta de estoque "
             "ou cliente apresentou interesse alem "
             "do produto no qual ligou sobre"
    )

    etq_insuficiente = fields.Boolean(
        string="Estoque insuficiente",
        help="Não atende ou atende "
             "parcialmente a demanda"
    )


    quantidade_requisitada = fields.Float(
        string="Quantidade requisitada",
    )

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        vetor = name.split(' ')

        records = []
        for rec in vetor:
            records.append('|')
            records.append('|')
            records.append('|')
            records.append('|')
            records.append('|')
            records.append(('name', operator, rec))
            records.append(('product_template_attribute_value_ids', operator, rec))
            records.append(('fipe_ids.name', operator, rec))
            records.append(('fipe_ids.marca', operator, rec))
            records.append(('fipe_ids.ano', operator, rec))
            records.append(('fipe_ids.codigo_fipe', operator, rec))
        if name:
            res = self.search(records)
            return res.name_get()
        return self.search([('name', operator, name)] + args, limit=limit).name_get()

    # def write(self, vals):
    #     if 'quantidade_requisitada' in vals:
    #         if vals['quantidade_requisitada'] > self.qty_available:
    #             raise UserError('O produto ' + self.name + ' tem estoque inferior a a quantidade requisitada.')
    #
    #     return super(InheritPreCompra, self).write(vals=vals)
