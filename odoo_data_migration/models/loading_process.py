from odoo import models, fields, api
import logging
from odoo.exceptions import ValidationError


logger = logging.getLogger(__name__)

class LoadingProcess(models.Model):
    _name = 'loading_process'
    _rec_name = 'tran_date_time'
    _description = 'Loading Process'

    tran_date_time = fields.Datetime(string="Transaction Date", required=True, )
    dbconnection = fields.Many2one(comodel_name="dbconnection", string="DB Connection", required=False, )
    action_type = fields.Selection(string="Action", selection=[('vendor_upload', 'Vendor upload'),
                                                               ('customer_upload', 'Customer upload'),
                                                               ('product_upload', 'Product Upload'),
                                                               ('product_categ_upload', 'Product Category Upload'),
                                                               ('product_invoices', 'Invoices Upload'),
                                                               ('product_brand_upload', 'Product Brand Upload'),
                                                               ('error', 'Error While Executing'),
                                                               ('database_connection', 'Database Connection'), ],
                                   required=False, )
    description = fields.Text(string="Description", required=False, )

    @api.model
    def create(self, vals):
        try:
            obj = super(LoadingProcess, self).create(vals)
        except Exception as e:
            logger.exception("create Method")
            raise ValidationError(e)
        return obj

    def write(self, vals):
        try:
            obj = super(LoadingProcess, self).write(vals)
        except Exception as e:
            logger.exception("Write Method")
            raise ValidationError(e)
        return obj

    def unlink(self):
        try:
            return super(LoadingProcess, self).unlink()
        except Exception as e:
            logger.exception("unlink Method")
            raise ValidationError(e)
