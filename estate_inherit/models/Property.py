from odoo import models

class Property(models.Model):
    _name = "estate.property"
    _inherit = [global,"mail.activity.mixin",'mail.thread']