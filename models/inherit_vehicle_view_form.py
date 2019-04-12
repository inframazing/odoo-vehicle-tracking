# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import Warning
import logging
import json
import urllib


class InheritVehicleViewForm(models.Model):
    _inherit = 'fleet.vehicle'

    # REVIEW: ¿Constraints for check size of dev_id?
    _sql_constraints = [
        ('dev_id_unique',
         'unique(dev_id)',
         'El Identificador ya está asignado a otro vehículo'
         )
    ]
    dev_id = fields.Char(string='Identificador')

    @api.one
    def act_get_data(self):
        # ===============Constants===============#
        URL_PORT = 'http://www.tyeye.net:8088/'
        API_ACT_LOGIN = 'StandardApiAction_login.action?account='
        ACCOUNT = 'HYFJMP20181012'
        PASS = '000000'
        API_ACT_STATUS = 'StandardApiAction_getDeviceStatus.action?jsession='
        DEV_ID = self.dev_id
        MAP = '&toMap=2&driver=0&geoaddress=1'
        # ===============BodyLogin===============#
        logging.getLogger("==========>DEV_ID<==========").info(self.dev_id)

        if self.dev_id is False:
            raise Warning(
                """
                Para rastrear un vehículo, primero asigne un identificador.
                """
                )

        elif len(self.dev_id) != 9:
            raise Warning(
                """
                El identificador debe contener 8 caracteres.
                """
                )

        body_login = URL_PORT + API_ACT_LOGIN + ACCOUNT + "&password=" + PASS
        response_login = urllib.urlopen(body_login)
        data_login = json.loads(response_login.read())
        jsession = data_login['jsession']
        logging.getLogger("==========>JSESSION<==========").info(jsession)
        # ===============Body Status===============#
        body_status = URL_PORT + API_ACT_STATUS + "&devIdno=" + DEV_ID + MAP
        response_status = urllib.urlopen(body_status)
        data_status = json.loads(response_status.read())
        date_time = data_status['status'][0]['gt']
        latitude = data_status['status'][0]['mlat']
        longitude = data_status['status'][0]['mlng']
        logging.getLogger("==========>DATETIME<==========").info(date_time)
        logging.getLogger("==========>LATITUDE<==========").info(latitude)
        logging.getLogger("==========>LONGITUDE<==========").info(longitude)

        track = self.env["vehicle.tracking"].create(dict(
            id_vehicle=self.id,
            date=date_time,
            time=date_time,
            latitude=latitude,
            longitude=longitude
        ))

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'vehicle.tracking',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': track.id
            # 'target': 'current',
        }

    @api.multi
    def vehicle_tracking_cron(self):
        vehicles_with_dev_id = self.env['fleet.vehicle'].search([('dev_id', '!=', False)])
        for x in vehicles_with_dev_id:
            x.act_get_data()
            logging.getLogger("==========>CRON IDS<==========").info(x.dev_id)
