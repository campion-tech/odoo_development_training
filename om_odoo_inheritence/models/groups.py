from odoo import models, fields, api


class ResGroups(models.Model):
    _inherit = "res.groups"

    def get_application_groups(self, domain):
        print("Domain+++++++++,", domain)
        group_id = self.env.ref('account.group_show_line_subtotals_tax_included').id
        lead_group_id = self.env.ref('crm.group_use_lead').id
        return super(ResGroups, self).get_application_groups(domain + [('id', 'not in', (group_id, lead_group_id))])