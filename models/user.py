from odoo import models, fields
from werkzeug.security import generate_password_hash

class CustomUser(models.Model):
    _name = 'custom.user'
    _description = 'Custom User'

    name = fields.Char(string='Name', required=True)
    login = fields.Char(string='Email', required=True)
    password = fields.Char(string='Password', required=True, write_only=True)  # Simpan hash password
    phone = fields.Char(string='Phone')
    groups_id = fields.Many2many('res.groups', string='Groups')

    def create(self, vals):
        # Hash the password before storing
        if 'password' in vals:
            vals['password'] = generate_password_hash(vals['password'])
        return super(CustomUser, self).create(vals)
