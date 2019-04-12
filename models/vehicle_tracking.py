# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import json


class VehicleTracking(models.Model):
    _name = "vehicle.tracking"
    _description = "Vehicle Tracking"

    def _compute_map(self):
        x = dict(position=dict(lat=self.latitude, lng=self.longitude), zoom=15)
        self.map = json.dumps(x)

    id_vehicle = fields.Many2one('fleet.vehicle', required=True, string='Eco.')
    date = fields.Date(string='Fecha', required=True, readonly=True, default=fields.Datetime.now)
    time = fields.Datetime(string='Hora', required=True, readonly=True, default=fields.Datetime.now)
    latitude = fields.Float(string='Latitud')
    longitude = fields.Float(string='Longitud')
    map = fields.Char(compute='_compute_map', store=False)
