from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    cancel_days = fields.Integer(string='Cancel Days', config_parameter='om_hospital.cancel_days')
#     we use ""config_parameter"" to save the data entered because we used a TransientModel
#     it gonna be saved in ((ir.config_parameter)) with ""om_hospital.cancel_days"" key