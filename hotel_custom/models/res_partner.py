# -*- coding: utf-8 -*-

from odoo import models, _, fields


class RESPartner(models.Model):
    _inherit = 'res.partner'

    is_owner = fields.Boolean('Owner')