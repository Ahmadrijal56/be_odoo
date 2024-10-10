# -*- coding: utf-8 -*-
# from odoo import http


# class BeProject(http.Controller):
#     @http.route('/be_project/be_project/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/be_project/be_project/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('be_project.listing', {
#             'root': '/be_project/be_project',
#             'objects': http.request.env['be_project.be_project'].search([]),
#         })

#     @http.route('/be_project/be_project/objects/<model("be_project.be_project"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('be_project.object', {
#             'object': obj
#         })
