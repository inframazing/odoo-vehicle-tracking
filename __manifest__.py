# -*- coding: utf-8 -*-

{
    'name': 'Rastreo de Vehículos',
    'version': '1.0',
    'category': 'Fleet',
    "": "'sequence': ''",
    'summary': 'Rastreo, Flotilla',
    'description': """""",
    'website': 'https://desiteg.com/portal/',
    'author': 'Desiteg-Tinny',
    'depends': ['base', 'fleet', 'esferica'],
    'data': [
        'data/ir_cron_actions.xml',
        'views/inherit_vehicle_view_form.xml',
        'views/vehicle_tracking.xml'
    ],
    "": "'test': []",
    "": "'demo': []",
    'installable': True,
    'auto_install': False,
    'application': True
}
