# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import http, SUPERUSER_ID
from odoo.http import request

class website_add_product(http.Controller):
    
    @http.route(['/shop/cart/update/product'], type='http', auth="public", methods=['GET'], website=True)
    def cart_update_product(self, product_id, add_qty=1, set_qty=0, **kw):
        try:
            add_qty = float(add_qty)
        except ValueError:
            return None
        if add_qty <= 0.0:
            return None
        request.website.sale_get_order(force_create=1)._cart_update(product_id=int(product_id), add_qty=add_qty, set_qty=float(set_qty))
        if request.httprequest.headers and request.httprequest.headers.get('Referer'):
            return request.redirect(str(request.httprequest.headers.get('Referer')))
        return request.redirect('/shop')
