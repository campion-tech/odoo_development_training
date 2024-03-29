from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    confirmed_user_id = fields.Many2one('res.users', string='Confirmed User')

    # inherit an existing function (def action_confirm) from sale.order
    def action_confirm(self):
       super(SaleOrder, self).action_confirm()
       self.confirmed_user_id = self.env.user.id
#        si on clique sur la bouton confirm, confirmed user prend l'utilisateur actuel de la base de donnée
