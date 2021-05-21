# -*- coding: utf-8 -*-
# from odoo import http


# class Drops(http.Controller):
#     @http.route('/drops/drops/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/drops/drops/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('drops.listing', {
#             'root': '/drops/drops',
#             'objects': http.request.env['drops.drops'].search([]),
#         })

#     @http.route('/drops/drops/objects/<model("drops.drops"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('drops.object', {
#             'object': obj
#         })
