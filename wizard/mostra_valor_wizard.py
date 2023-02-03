from odoo import models, fields, api, _
from datetime import date
from odoo.exceptions import UserError


class MostraValorWizard(models.TransientModel):
    _name = "mostra.valor.wizard"


    cliente = fields.Many2one(
        'res.partner',
        string="Cliente"
    )

    data_vencimento_cotacao = fields.Date(
        string="Data",
    )


    produto_desejado_id = fields.Many2one(
        'product.product',
        string="Produto desejado"
    )

    quantidade_requisitada_related = fields.Float(
        string="Quantidade requisitada",
        related="produto_desejado_id.quantidade_requisitada",
        default=None,
        help="Este campo é do inherit do product product",
        readonly=False
    )

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


    quantidade_requisitada = fields.Float(
        string="Quantidade requisitada",
        default=None
    )

    produto_desejado_quantidade_related = fields.Float(
        related="produto_desejado_id.virtual_available",
        string="Estoque"
    )

    # _____-------=====Campos relacionados as variantes de produto=====-------_____

    variantes_produto_desejado_ids = fields.Many2one(
        'product.product',
        string="Variantes do produto",

    )

    quantidade_variante_requisitada = fields.Float(
        related="variantes_produto_desejado_ids.quantidade_requisitada",
        string="Quantidade requisitada",
        readonly=False
    )
    estoque_variante = fields.Float(
        related="variantes_produto_desejado_ids.virtual_available",
        string="Estoque variante"
    )
    valor_variante = fields.Float(
        related="variantes_produto_desejado_ids.lst_price",
        string="Valor variante"
    )

    # _____-------=====Campos relacionados ao produto alternativo=====-------_____

    produto_alternativo_id = fields.Many2one(
        'product.product',
        string="Produto alternativo",
    )

    produto_alternativo_related_valor_id = fields.Float(
        related='produto_alternativo_id.lst_price',
        string="Valor"
    )


    quantidade_alternativo_requisitada = fields.Float(
        related="produto_alternativo_id.quantidade_requisitada",
        string="Quantidade requisitada",
        readonly=False
    )

    estoque_alternativo = fields.Float(
        related="produto_alternativo_id.virtual_available",
        string="Estoque alternativo"
    )
    valor_alternativo = fields.Float(
        related="produto_alternativo_id.lst_price",
        string="Valor variante"
    )

    acessorio_desejado = fields.Many2many(
        'product.product',
        relation="rel_acessorio_desejado_product",
        string="Acessorios do produto",
        domain="[('virtual_available','>',0)]"
    )

    acessorio_variante = fields.Many2many(
        'product.product',
        relation="rel_acessorio_variante_product",
        string="Acessorios do produto",
        domain="[('virtual_available','>',0)]"
    )

    acessorio_alternativo = fields.Many2many(
        'product.product',
        relation="rel_acessorio_alternativo_product",
        string="Acessorios do produto",
        domain="[('virtual_available','>',0)]"
    )

    carrinho_ids = fields.Many2many(
        'product.product',
        relation='rel_carrinho_product_mostra_valor',
        string="Carrinho"
    )

    carrinho_geral_ids = fields.Many2many(
        'product.product',
        relation='rel_carrinho_geral_product_mostra_valor',
        string="Carrinho geral",
        help="Este carrinho agrupa todos os produtos, os que"
             " o cliente teve interesse e os que serão de "
             "fato comprados"
    )

    # _____-------=====Booleans que são usados como controle são passados da primeira pra segunda tela=====-------_____

    desejado_check = fields.Boolean()
    variante_check = fields.Boolean()
    alternativo_check = fields.Boolean()
    desejado_insuficiente = fields.Boolean()
    e_um_alternativo = fields.Boolean()

    #estas 3 variaveis fazem a mesma coisa são usadas para sumir com um goup que
    # possui um aviso ao usuario tive que usar tres pois por algum motivo quando
    # eu usava a mesma os capos que eu queria não funcionavam

    some_enviar = fields.Boolean()
    some_enviar_variante = fields.Boolean()
    some_enviar_alternativo = fields.Boolean()

    # _____-------=====Funções de validação dos campos de acessorio=====-------_____

    @api.onchange('acessorio_desejado')
    def valida_acessorio_desejado(self):
        if self.acessorio_desejado.quantidade_requisitada > self.acessorio_desejado.virtual_available:
            raise UserError('Algum dos produtos no campo de acessorios esta com quantidade requisitada maior que o estoque do mesmo')
        if self.acessorio_desejado.quantidade_requisitada == 0:
            self.acessorio_desejado.vai_comprar = False
        elif self.acessorio_desejado.quantidade_requisitada != 0:
            self.acessorio_desejado.vai_comprar = True

    @api.onchange('acessorio_variante')
    def valida_acessorio_variante(self):
        if self.acessorio_variante.quantidade_requisitada > self.acessorio_variante.virtual_available:
            raise UserError(
                'Algum dos produtos no campo de acessorios esta com quantidade requisitada maior que o estoque do mesmo')
        if self.acessorio_variante.quantidade_requisitada == 0:
            self.acessorio_variante.vai_comprar = False
        elif self.acessorio_variante.quantidade_requisitada != 0:
            self.acessorio_variante.vai_comprar = True

    @api.onchange('acessorio_alternativo')
    def valida_acessorio_alternativo(self):
        if self.acessorio_alternativo.quantidade_requisitada > self.acessorio_alternativo.virtual_available:
            raise UserError(
                'Algum dos produtos no campo de acessorios esta com quantidade requisitada maior que o estoque do mesmo')
        if self.acessorio_alternativo.quantidade_requisitada == 0:
            self.acessorio_alternativo.vai_comprar = False
        elif self.acessorio_alternativo.quantidade_requisitada != 0:
            self.acessorio_alternativo.vai_comprar = True

    # _____-------=====funçoes de validação da quantidade requirida pelo cliente=====-------_____

    @api.onchange('quantidade_requisitada_related')
    def valor_adequado_desejado(self):
        if self.quantidade_requisitada_related == 0:
            self.produto_desejado_id.vai_comprar = False
        else:
            self.produto_desejado_id.vai_comprar = True
        if self.produto_desejado_id:
            for rec in self.produto_desejado_id.accessory_product_ids:
                self.acessorio_desejado = [(6, 0, [rec.id])]
        if self.quantidade_requisitada_related > self.produto_desejado_id.virtual_available:
            self.produto_desejado_id.etq_insuficiente = True
            self.desejado_insuficiente = True
            self.some_enviar = True

        elif self.quantidade_requisitada_related <= self.produto_desejado_id.virtual_available:
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

        if self.quantidade_variante_requisitada > self.variantes_produto_desejado_ids.virtual_available:
            if self.desejado_insuficiente:
                self.variantes_produto_desejado_ids.alt_flt_estoque = True
            self.variantes_produto_desejado_ids.etq_insuficiente = True
            self.some_enviar_variante = True

        elif self.quantidade_variante_requisitada <= self.variantes_produto_desejado_ids.virtual_available:
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
        if self.quantidade_alternativo_requisitada > self.produto_alternativo_id.virtual_available:
            self.produto_alternativo_id.etq_insuficiente = True
            self.some_enviar_alternativo = True

        elif self.quantidade_variante_requisitada <= self.variantes_produto_desejado_ids.virtual_available:
            self.some_enviar_alternativo = False

    # _____-------=====As funções a seguir voltam pra primeira tela=====-------_____

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
            'default_data_vencimento_cotacao': self.data_vencimento_cotacao,
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
            'default_data_vencimento_cotacao': self.data_vencimento_cotacao,
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
            'default_data_vencimento_cotacao': self.data_vencimento_cotacao,
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
