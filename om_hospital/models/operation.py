from odoo import api, fields, models, _


class HospitalOperation(models.Model):
    _name = "hospital.operation"
    _description = "Hospital Operation"
    _log_access = False
    _order = 'id desc'

    doctor_id = fields.Many2one('res.users', string='Doctor')
    operation_name = fields.Char(string="Name")
    reference_record = fields.Reference(selection=[('hospital.patient', 'Patient'), ('hospital.appointment', 'Appointment')], string="Record")


    @api.model
    def name_create(self, name):
        print("name+++++++++", name)
        return self.create({'operation_name': name}).name_get()[0]
    # cette fonction donne le droit de créé une opération de la fenetre "patient".
    # on n'a pas le droit de crée une opération dans un field many2one parceque cette class n'a pas d'un name ou _rec_name