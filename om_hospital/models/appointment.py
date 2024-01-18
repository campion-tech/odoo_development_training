from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointments"
    _rec_name = 'sequence'
    _order = 'id desc'

    patient_id = fields.Many2one('hospital.patient', string="Patient", ondelete="cascade")
    # ondelete="cascade" ==> if we delete a patient, his appointments will be deleted automatically
    # ondelete="restrict" ==> if we want to delete a patient have appointments, an error message will appear
    gender = fields.Selection(related='patient_id.gender')
    appointment_time = fields.Datetime(string='Appointment Time', default=fields.Datetime.now)
    booking_date = fields.Date(string='Booking Date', default=fields.Date.context_today)
    ref = fields.Char(string='Reference', help="Reference from patient record")
    sequence = fields.Char(string= 'Sequence')
    prescription = fields.Html(string='Prescription')
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')], default='draft', string="Status", required=True)
    doctor_id = fields.Many2one('res.users', string='Doctors', tracking=True)
    pharmacy_lines_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id', string='Pharmacy Lines')
    hide_sales_price = fields.Boolean(string="Hide Sales Price")
    active = fields.Boolean(string="Active", default=True)

    operation = fields.Many2one('hospital.operation', string='Operations', tracking=True)

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref
    # onchange function used to bring reference from hospital.patient to hospital.appointment



    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        return super(HospitalAppointment, self).create(vals)

    def unlink(self):
        print("Test...................")
        for rec in self:
            if rec.state != 'draft':
                raise ValidationError(_("You cannot delete appointment only in 'Draft' or 'In Consultation' status."))
        return super(HospitalAppointment, self).unlink()

    def write(self, vals):
        print("write method is treggered", vals)
        if not self.sequence and not vals.get('sequence'):
            # si sequence est vide et sequence ne contient pas de valeur
            vals['sequence'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        return super(HospitalAppointment, self).write(vals)
    # this function add a sequence to appointment that don't have it if we press "edit" button


    def action_test(self):
        print("Button clicked!!!!!")
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Click Successfull',
                'type': 'rainbow_man',
            }
        }


    def action_in_consultation(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'in_consultation'
    # this function is for "in consultation" button

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        action = self.env.ref('om_hospital.action_cancel_appointment').read()[0]
        return action
        # bouton cancel de type object peut se fonctionne comme un bouton de type action
        # or
        # for rec in self:
        #     rec.state = 'cancel'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'


class AppointmentPharmacyLines(models.Model):
    _name = "appointment.pharmacy.lines"
    _description = "Appointment Pharmacy Lines"

    product_id = fields.Many2one('product.product', required=True)
    price_unit = fields.Float(related='product_id.list_price')
    qty = fields.Integer(string='Quantity', default=1)
    appointment_id = fields.Many2one('hospital.appointment', string='Appointments')