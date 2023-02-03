{
    'name': 'Cotação',
    'version': '1.1',
    'author': 'Thiago Francelino',
    'summary': '',
    'sequence': '1',
    'description': 'Cotação',
    'category': 'pagamento',
    # 'depends': ['base', 'sale_management', 'stock'],
    'depends': ['sale_management'],
    # 'depends': ['account', 'project_requests', 'cadastro_cheque'],
    'data': [
        "security/ir.model.access.csv",
        "wizard/cotacao_wizard_view.xml",
        "wizard/mostra_valor_wizard_view.xml",
        "views/inherit_sale_order_view.xml",
        "views/carrinho_view.xml",
    ],
}
