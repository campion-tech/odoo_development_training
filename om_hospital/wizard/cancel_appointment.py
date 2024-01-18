import datetime
from odoo import api, fields, models, _
from dateutil import relativedelta
from datetime import date
from odoo.exceptions import ValidationError


class CancelAppointementWizard(models.TransientModel):
    _name = "cancel.appointement.wizard"
    _description = "Cancel Appointement Wizard"
    
    @api.model
    def default_get(self, fields):
        res = super(CancelAppointementWizard, self).default_get(fields)
        res['date_cancel'] = datetime.date.today()
        if self.env.context.get('active_id'):
            res['appointment_id'] = self.env.context.get('active_id')
        return res

    appointment_id = fields.Many2one('hospital.appointment', string="Appointment",
                                     domain=[('state', '=', 'draft'), ('priority', 'in', (0,1))])
    reason = fields.Text(string="Reason")
    date_cancel = fields.Date(string="Cancellation Date") #, default=fields.Date.context_today

    def action_cancel(self):
        cancel_day = self.env['ir.config_parameter'].get_param('om_hospital.cancel_days')
        print("cancel_day", cancel_day)
        allowed_date = self.appointment_id.booking_date + relativedelta.relativedelta(days=int(cancel_day))
        if cancel_day != 0 and allowed_date < date.today():
            raise ValidationError(_("Sorry, cancellation is not allowed for this booking!"))
        self.appointment_id.state = 'cancel'
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

        # if self.appointment_id.booking_date == fields.Date.today():
        #     raise ValidationError("Sorry, cancellation is not allowed on the same day of booking")
        # self.appointment_id.state = 'cancel'
        # return
