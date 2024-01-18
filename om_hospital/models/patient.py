from datetime import date
from odoo import api, fields, models,_
from odoo.exceptions import ValidationError
from dateutil import relativedelta


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Patient"



    name = fields.Char(string='Name', tracking=True)
    date_of_birth = fields.Date(string='Date Of Birth')
    ref = fields.Char(string='Reference')
    age = fields.Integer(string="Age", tracking=True, compute='_compute_age', inverse='_inverse_compute_age',
                         search='_search_age')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    active = fields.Boolean(string="Active", default=True)
    # appointment_id = fields.Many2one('hospital.appointment', string='Appointments')
    image = fields.Image(string="Image")
    tag_ids = fields.Many2many('patient.tag', string="Tags")
    appointment_count = fields.Integer(string="Appointment Count", compute='_compute_appointment_count', store='True')
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointments")
    parent = fields.Char(string="Parent")
    marital_status = fields.Selection([('married', 'Married'), ('single', 'Single')], string="Marital Status", tracking=True)
    partner_name = fields.Char(string="Partner Name")
    is_birthday = fields.Boolean(string="Birthday ?", compute='compute_is_birthday')
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    website = fields.Char(string="Website")


    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])
    # this function count the number of appointments for each patient



    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError("The entered date of birth is not acceptable!")
    


    @api.ondelete(at_uninstall=False)
    def _check_appointments(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError(_("You cannot delete a patient with appointments !"))



    # def name_get(self):
    #     result = []
    #     for record in self:
    #         new_name = record.ref + " " + record.name
    #         result.append((record.id, new_name))
    #     print("name_get : ", result)
    #     return result

    # result = super(HospitalPatient, self).name_get()
    # or replace this code with:
    def name_get(self):
        return [(record.id, "%s %s" % (record.ref, record.name)) for record in self]
    # This is shown in the suggestion list for selecting exact patients from two or more patients that have the same name.
    # This process of obtaining internal reference with the patient name in the patient list is done using the name_get() function

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        print("self:",self)
        print("vals:",vals)
        # to creat sequence by ref field
        # hospital.patient c'est le " code " dans le fichier sequence_data.xml
        return super(HospitalPatient, self).create(vals)

    def write(self, vals):
        print("write method is treggered", vals)
        if not self.ref and not vals.get('ref'):
            # si ref est vide et ref ne contient pas de valeur
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).write(vals)


    @api.depends('date_of_birth')
    # @api.depends called Decorator
    def _compute_age(self):
        print("the self:.. ", self)
        for rec in self:
            today = date.today()
            print(today)
            if rec.date_of_birth:
               rec.age = today.year - rec.date_of_birth.year
            else:
               rec.age = 0


    def _inverse_compute_age(self):
        today = date.today()
        for rec in self:
            if not rec.date_of_birth:
                rec.date_of_birth = today - relativedelta.relativedelta(years=rec.age)
    # we use this function to make age field editable

    def _search_age(self, operator, value):
        date_of_birth = date.today() - relativedelta.relativedelta(years=value)
        start_of_year = date_of_birth.replace(day=1,month=1)
        end_of_year = date_of_birth.replace(day=31,month=12)
        return [('date_of_birth', '>=', start_of_year), ('date_of_birth', '<=', end_of_year)]
    # we use this function to make age stored field in the database



    def action_done(self):
        print("Clicked**************")
        return

    @api.depends('date_of_birth')
    def compute_is_birthday(self):
        for rec in self:
            is_birthday = False
            if rec.date_of_birth:
                today = date.today()
                if today.day == rec.date_of_birth.day and today.month == rec.date_of_birth.month:
                    is_birthday = True
            rec.is_birthday = is_birthday


