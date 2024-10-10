from odoo import models, fields

class CustomUser(models.Model):
    _name = 'custom.user'
    _description = 'Custom User'

    name = fields.Char(string='Name', required=True)
    login = fields.Char(string='Email', required=True)
    password = fields.Char(string='Password')
    phone = fields.Char(string='Phone')
    groups_id = fields.Many2many('res.groups', string='User Groups')
