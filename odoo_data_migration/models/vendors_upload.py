from odoo import models, fields, api
import logging
from odoo.exceptions import ValidationError
import datetime

logger = logging.getLogger(__name__)

class VendorsUpload(models.Model):
    _name = 'vendors_upload'
    _rec_name = 'name'
    _description = 'Upload Odoo Vendors'

    name = fields.Char()

    @api.model
    def create(self, vals):
        try:
            obj = super(VendorsUpload, self).create(vals)
        except Exception as e:
            logger.exception("create Method")
            raise ValidationError(e)
        return obj

    def write(self, vals):
        try:
            obj = super(VendorsUpload, self).write(vals)
        except Exception as e:
            logger.exception("Write Method")
            raise ValidationError(e)
        return obj

    def unlink(self):
        try:
            return super(VendorsUpload, self).unlink()
        except Exception as e:
            logger.exception("unlink Method")
            raise ValidationError(e)