# -*- coding: utf-8 -*-

{
    'name': 'Hospital Management',
    'version': '1.0.0',
    'category': 'Hospital',
    'author': 'Campion-Tech',
    'sequence': -100,
    'summary': 'Hospital management system',
    'description': """""",
    'depends': ['mail', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'data/patient_tag_data.xml',
        'data/sequence_data.xml',
        'data/patient.tag.csv',
        'wizard/cancel_appointment_view.xml',
        'views/menu.xml',
        'views/patient_view.xml',
        'views/female_patient_view.xml',
        'views/appointment_view.xml',
        'views/patient_tag.xml',
        'views/odoo_playground_view.xml',
        'views/res_config_settings_views.xml',
        'views/operation_view.xml',

    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'assets': {},
    'license': 'LGPL-3',
}
