from odoo import models, fields, api, _
from odoo.exceptions import UserError

class InheritResPartner(models.Model):


    _inherit = 'res.partner'


    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        vetor = name.split(' ')

        records = []
        for rec in vetor:
            records.append('|')
            records.append('|')
            records.append(('name', operator, rec))
            records.append(('route_id.nome_rota', operator, rec))
            records.append(('cod_hitec', operator, rec))
        if name:
            res = self.search(records)
            return res.name_get()
        return self.search([('name', operator, name)] + args, limit=limit).name_get()