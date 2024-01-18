from odoo import _, api, fields, models


class PatientTag(models.Model):
    _name = "patient.tag"
    _description = "Patient Tag"



    name = fields.Char(string='Name', tracking=True)
    active = fields.Boolean(string='Active', default=True, copy=False)
    color = fields.Integer(string='Color')
    color_2 = fields.Char(string='Color 2')
    sequence = fields.Integer(string='Sequence')

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = _("%s (copy)", self.name)
        #     " _ " we put it for translation
        return super(PatientTag, self).copy(default)

    _sql_constraints = [
        ('unique_tag_name', 'unique(name, active)', 'Name must be unique.'),
        ('check_sequence', 'check(sequence > 0)', 'Sequence must be non zero positive number.')
    ]
    # _sql_constraints used when we have to validate and check data entered by user
    # ('condition_name', 'condition(field_name)', 'error message.')
