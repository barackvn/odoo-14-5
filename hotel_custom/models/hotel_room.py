# -*- coding: utf-8 -*-

from odoo import models, fields


class HotelRoom(models.Model):
    _inherit = 'product.product'

    owner_id = fields.Many2one('res.partner', string='Owner', domain=[('is_owner', '=', True)])
