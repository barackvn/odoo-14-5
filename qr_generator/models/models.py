# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import qrcode
import base64
import io


class QRGenerator(models.Model):
    _name = 'qr.generator'

    @api.model
    def get_qr_code(self, data):
        if data != "":
            img = qrcode.make(data)
            result = io.BytesIO()
            img.save(result, format='PNG')
            result.seek(0)
            img_bytes = result.read()
            base64_encoded_result_bytes = base64.b64encode(img_bytes)
            base64_encoded_result_str = base64_encoded_result_bytes.decode('ascii')
            return base64_encoded_result_str
