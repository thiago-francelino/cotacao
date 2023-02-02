from odoo import models, fields, api, _
from datetime import date
from odoo.exceptions import UserError


class MostraValorWizard(models.TransientModel):
    _name = "mostra.valor.wizard"

    name = fields.Char(
        string="ai pai para"
    )

    cliente = fields.Many2one(
        'res.partner',
        string="Cliente"
    )

    rota_id = fields.Many2one(
        'routes',
        string="Rotas do cliente"
    )

    data_vencimento_cotacao = fields.Date(
        string="Data",
        default=date.today()
    )

    condicao_de_pagamento = fields.Selection(
        [('dinheiro', 'Dinheiro'),
         ('pix', 'PIX'),
         ('cheque', 'Cheque')],
        string="Condição de pagamento"
    )

    produto_desejado_id = fields.Many2one(
        'product.product',
        string="Produto desejado"
    )

    # produto_alternativo_id = fields.Many2one(
    #     'product.product',
    #     string="Produto alternativo"
    # )

    carrinho_ids = fields.Many2many(
        'product.product',
        relation='rel_carrinho_product_mostra_valor',
        string="Carrinho"
    )

    e_um_alternativo = fields.Boolean()

    produto_desejado_related_valor_id = fields.Float(
        related='produto_desejado_id.lst_price',
        string="Valor"
    )

    produto_desejado_quantidade_desejada_id = fields.Float(
        related='produto_desejado_id.quantidade_requisitada',
        string="Quantidade requisitada",
        readonly=False,
        store=True,
    )

    produto_alternativo_related_valor_id = fields.Float(
        related='produto_alternativo_id.lst_price',
        string="Valor"
    )

    # accessory_product_related_ids = fields.Many2many(
    #     related='produto_desejado_id.accessory_product_ids',
    #     string="Acessorios do produto"
    # )

    carrinho_geral_ids = fields.Many2many(
        'product.product',
        relation='rel_carrinho_geral_product_mostra_valor',
        string="Carrinho geral",
        help="Este carrinho agrupa todos os produtos, os que"
             " o cliente teve interesse e os que serão de "
             "fato comprados"
    )

    quantidade_requisitada = fields.Float(
        string="Quantidade requisitada",
        default=None
    )

    opcoes_estoque = fields.Boolean()

    soma_pecas = fields.Integer(
        string="Quantidade de peças"
    )

    soma_valor = fields.Integer(
        string="Valor total",
        default=0
    )
    pre_carrinho = fields.Many2many(
        'product.product',
        relation='rel_pre_carrinho_product_mostra_valor',
        string="Pre carrinho",
        help="Este carrinho agrupa "
    )

    produto_desejado_quantidade_related = fields.Float(
        related="produto_desejado_id.qty_available",
        string="Estoque"
    )


    variantes_produto_desejado_ids = fields.Many2one(
        'product.product',
        string="Variantes do produto",

    )

    produto_alternativo_id = fields.Many2one(
        'product.product',
        string="Produto alternativo",
    )


    qtd_cliente_info = fields.Integer(
        string="Quantidade requerida"
    )

    etq_insuficiente_related = fields.Boolean(
        related="produto_desejado_id.etq_insuficiente"
    )

    quantidade_requisitada_related = fields.Float(
        string="Quantidade requisitada",
        related="produto_desejado_id.quantidade_requisitada",
        default=None,
        help="Este campo é do inherit do product product",
        readonly=False
    )
    quantidade_alternativo_requisitada = fields.Float(related="produto_alternativo_id.quantidade_requisitada",
                                                      string="Quantidade requisitada",
                                                      readonly=False)

    quantidade_variante_requisitada = fields.Float(related="variantes_produto_desejado_ids.quantidade_requisitada",
                                                   string="Quantidade requisitada",
                                                   readonly=False)
    estoque_variante = fields.Float(related="variantes_produto_desejado_ids.qty_available", string="Estoque variante")
    valor_variante = fields.Float(related="variantes_produto_desejado_ids.lst_price", string="Valor variante")

    estoque_alternativo = fields.Float(related="produto_alternativo_id.qty_available", string="Estoque alternativo")
    valor_alternativo = fields.Float(related="produto_alternativo_id.lst_price", string="Valor variante")

    # acessorio_desejado = fields.Many2many(
    #     related='produto_desejado_id.accessory_product_ids',
    #     relation="rel_acessorio_desejado_product",
    #     string="Acessorios do produto"
    # )
    #
    # acessorio_variante = fields.Many2many(
    #     related='variantes_produto_desejado_ids.accessory_product_ids',
    #     relation="rel_acessorio_variante_product",
    #     string="Acessorios do produto"
    # )
    #
    # acessorio_alternativo = fields.Many2many(
    #     related='produto_alternativo_id.accessory_product_ids',
    #     relation="rel_acessorio_alternativo_product",
    #     string="Acessorios do produto"
    # )

    acessorio_desejado = fields.Many2many(
        'product.product',
        relation="rel_acessorio_desejado_product",
        string="Acessorios do produto"
    )

    acessorio_variante = fields.Many2many(
        'product.product',
        relation="rel_acessorio_variante_product",
        string="Acessorios do produto"
    )

    acessorio_alternativo = fields.Many2many(
        'product.product',
        relation="rel_acessorio_alternativo_product",
        string="Acessorios do produto"
    )

    desejado_check = fields.Boolean()
    variante_check = fields.Boolean()
    alternativo_check = fields.Boolean()
    desejado_insuficiente = fields.Boolean()
    variante_insuficiente = fields.Boolean()


    some_enviar = fields.Boolean()
    some_enviar_variante = fields.Boolean()
    some_enviar_alternativo = fields.Boolean()

    # tentativa de mostrar valor customizado no wizard de mostra valor

    descricao_do_valor_alternativo = 'O valor do produto alternativo: ' + str(
        produto_alternativo_id.name) + ' é: ' + str(produto_alternativo_related_valor_id)
    descricao_do_valor_desejado = 'O valor do produto alternativo: ' + str(produto_desejado_id.name) + ' é: ' + str(
        produto_desejado_related_valor_id)

    # @api.mult
    # @api.multi

    @api.onchange('acessorio_desejado')
    def valida_acessorio_desejado(self):
        if self.acessorio_desejado.quantidade_requisitada > self.acessorio_desejado.qty_available:
            raise UserError('Algum dos produtos no campo de acessorios esta com quantidade requisitada maior que o estoque do mesmo')

    @api.onchange('acessorio_variante')
    def valida_acessorio_variante(self):
        if self.acessorio_variante.quantidade_requisitada > self.acessorio_variante.qty_available:
            raise UserError(
                'Algum dos produtos no campo de acessorios esta com quantidade requisitada maior que o estoque do mesmo')

    @api.onchange('acessorio_alternativo')
    def valida_acessorio_alternativo(self):
        if self.acessorio_alternativo.quantidade_requisitada > self.acessorio_alternativo.qty_available:
            raise UserError(
                'Algum dos produtos no campo de acessorios esta com quantidade requisitada maior que o estoque do mesmo')


    @api.onchange('quantidade_requisitada_related')
    def valor_adequado_desejado(self):
        if self.quantidade_requisitada_related == 0:
            self.produto_desejado_id.vai_comprar = False
        else:
            self.produto_desejado_id.vai_comprar = True
        if self.produto_desejado_id:
            for rec in self.produto_desejado_id.accessory_product_ids:
                self.acessorio_desejado = [(6, 0, [rec.id])]
        if self.quantidade_requisitada_related > self.produto_desejado_id.qty_available:
            self.produto_desejado_id.etq_insuficiente = True
            self.desejado_insuficiente = True
            self.some_enviar = True
            self.produto_desejado_id.quantidade_requisitada = self.qtd_cliente_info

        elif self.quantidade_requisitada_related <= self.produto_desejado_id.qty_available:
            self.some_enviar = False

    @api.onchange('quantidade_variante_requisitada')
    def valor_adequado_variante(self):
        if self.quantidade_variante_requisitada == 0:
            self.variantes_produto_desejado_ids.vai_comprar = False
        else:
            self.variantes_produto_desejado_ids.vai_comprar = True
        if self.variantes_produto_desejado_ids:
            for rec in self.variantes_produto_desejado_ids.accessory_product_ids:
                self.acessorio_variante = [(6, 0, [rec.id])]

        if self.quantidade_variante_requisitada > self.variantes_produto_desejado_ids.qty_available:
            if self.desejado_insuficiente:
                self.variantes_produto_desejado_ids.alt_flt_estoque = True
            self.variantes_produto_desejado_ids.etq_insuficiente = True
            self.variante_insuficiente = True
            self.some_enviar_variante = True
            # self.variantes_produto_desejado_ids.quantidade_variante_requisitada = self.qtd_cliente_info

        elif self.quantidade_variante_requisitada <= self.variantes_produto_desejado_ids.qty_available:
            if self.desejado_insuficiente:
                self.variantes_produto_desejado_ids.alt_flt_estoque = True
            self.some_enviar_variante = False

    @api.onchange('quantidade_alternativo_requisitada')
    def valor_adequado_alternativo(self):
        if self.quantidade_alternativo_requisitada == 0:
            self.produto_alternativo_id.vai_comprar = False
        else:
            self.produto_alternativo_id.vai_comprar = True
        if self.produto_alternativo_id:
            for rec in self.produto_alternativo_id.accessory_product_ids:
                self.acessorio_alternativo = [(6, 0, [rec.id])]
        if self.quantidade_alternativo_requisitada > self.produto_alternativo_id.qty_available:
            self.produto_alternativo_id.etq_insuficiente = True
            self.some_enviar_alternativo = True
            if self.variante_insuficiente:
                self.produto_alternativo_id.alt_flt_variante = True
            # self.produto_alternativo_id.quantidade_alternativo_requisitada = self.qtd_cliente_info

        elif self.quantidade_variante_requisitada <= self.variantes_produto_desejado_ids.qty_available:
            self.some_enviar_alternativo = False

    # @api.onchange('variantes_produto_desejado_ids')
    # def valor_adequado_variante(self):


    def wizard_volta_cotacao_variante(self):
        vetor = []
        vetor_geral = []


        for rec1 in self.carrinho_ids.ids:
            vetor.append(rec1)

        for rec2 in self.carrinho_geral_ids.ids:
            vetor_geral.append(rec2)

        if self.acessorio_desejado:
            for rec in self.acessorio_desejado:
                vetor_geral.append(rec.id)
                vetor.append(rec.id)

        vetor_geral.append(self.produto_desejado_id.id)
        vetor.append(self.produto_desejado_id.id)

        ctx = dict()
        ctx.update({
            'default_cliente': self.cliente.id,
            'default_rota_id': self.rota_id.id,
            'default_data_vencimento_cotacao': self.data_vencimento_cotacao,
            'condicao_de_pagamento': self.condicao_de_pagamento,
            'default_carrinho_ids': vetor,
            'default_carrinho_geral_ids': vetor_geral,
            'default_variante_check': True,
            'default_alternativo_check': self.alternativo_check,
            'default_temp': vetor_geral,
            'default_produto_desejado_id': self.produto_desejado_id.id,
            'default_desejado_insuficiente': self.desejado_insuficiente,
            'default_variantes_produto_desejado_ids': False,
            'default_produto_alternativo_id': False,
            'default_desejado_check': False,
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'nome',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'cotacao.wizard',
            'views': [
                [
                    self.env.ref("cotacao.cotacao_wizard_form").id,
                    'form']
            ],
            'context': ctx,
            'target': 'new'
        }

    def wizard_volta_cotacao_todas_opcoes(self):
        vetor = []
        vetor_geral = []
        for rec1 in self.carrinho_ids.ids:
            vetor.append(rec1)

        for rec2 in self.carrinho_geral_ids.ids:
            vetor_geral.append(rec2)

        if self.acessorio_variante:
            for rec in self.acessorio_variante:
                vetor_geral.append(rec.id)
                vetor.append(rec.id)

        if self.variantes_produto_desejado_ids:
            if self.desejado_insuficiente:
                self.variantes_produto_desejado_ids.alt_flt_estoque = True
                vetor_geral.append(self.variantes_produto_desejado_ids.id)
                vetor.append(self.variantes_produto_desejado_ids.id)
            else:
                self.variantes_produto_desejado_ids.alt_flt_estoque = False
                vetor_geral.append(self.variantes_produto_desejado_ids.id)
                vetor.append(self.variantes_produto_desejado_ids.id)


        ctx = dict()
        ctx.update({
            'default_cliente': self.cliente.id,
            'default_rota_id': self.rota_id.id,
            'default_data_vencimento_cotacao': self.data_vencimento_cotacao,
            'condicao_de_pagamento': self.condicao_de_pagamento,
            'default_produto_desejado_id': self.produto_desejado_id.id,
            'default_carrinho_ids': vetor,
            'default_carrinho_geral_ids': vetor_geral,
            'default_temp': vetor_geral,
            'default_variantes_produto_desejado_ids': False,
            'default_produto_alternativo_id': False,
            'default_variante_check': True,
            'default_alternativo_check': True,
            'default_produto_desejado_id': self.produto_desejado_id.id
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'nome',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'cotacao.wizard',
            'views': [
                [
                    self.env.ref("cotacao.cotacao_wizard_form").id,
                    'form']
            ],
            'context': ctx,
            'target': 'new'
        }

    def wizard_volta_cotacao_final(self):
        vetor = []
        vetor_geral = []
        for rec1 in self.carrinho_ids.ids:
            vetor.append(rec1)

        for rec2 in self.carrinho_geral_ids.ids:
            vetor_geral.append(rec2)



        if self.produto_desejado_id:
            vetor_geral.append(self.produto_desejado_id.id)
            vetor.append(self.produto_desejado_id.id)

        if self.acessorio_desejado:
            for rec in self.acessorio_desejado:
                vetor_geral.append(rec.id)
                vetor.append(rec.id)



        if self.acessorio_variante:
            for rec in self.acessorio_variante:
                vetor_geral.append(rec.id)
                vetor.append(rec.id)

        if self.variantes_produto_desejado_ids:
            if self.desejado_insuficiente:
                self.variantes_produto_desejado_ids.alt_flt_estoque.alt_flt_estoque = True
                vetor_geral.append(self.variantes_produto_desejado_ids.id)
                vetor.append(self.variantes_produto_desejado_ids.id)
            else:
                self.variantes_produto_desejado_ids.alt_flt_estoque = False
                vetor_geral.append(self.variantes_produto_desejado_ids.id)
                vetor.append(self.variantes_produto_desejado_ids.id)



        if self.acessorio_alternativo:
            for rec in self.acessorio_alternativo:
                vetor_geral.append(rec.id)
                vetor.append(rec.id)

        if self.produto_alternativo_id:
            if self.desejado_insuficiente:
                self.produto_alternativo_id.alt_flt_estoque = True
                vetor_geral.append(self.produto_alternativo_id.id)
                vetor.append(self.produto_alternativo_id.id)
            else:
                self.produto_alternativo_id.alt_flt_estoque = False
                vetor_geral.append(self.produto_alternativo_id.id)
                vetor.append(self.produto_alternativo_id.id)

        ctx = dict()
        ctx.update({
            'default_cliente': self.cliente.id,
            'default_rota_id': self.rota_id.id,
            'default_data_vencimento_cotacao': self.data_vencimento_cotacao,
            'condicao_de_pagamento': self.condicao_de_pagamento,
            'default_carrinho_ids': vetor,
            'default_temp': vetor_geral,
            'default_carrinho_geral_ids': vetor_geral,
            'default_variante_check': False,
            'default_alternativo_check': False,
            'default_produto_desejado_id': self.produto_desejado_id.id,
            'default_variantes_produto_desejado_ids': False,
            'default_produto_alternativo_id': False,
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'nome',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'cotacao.wizard',
            'views': [
                [
                    self.env.ref("cotacao.cotacao_wizard_form").id,
                    'form']
            ],
            'context': ctx,
            'target': 'new'
        }
