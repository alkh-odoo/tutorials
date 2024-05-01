from odoo import models, fields

class User(models.Model):
    
    _inherit = 'res.users'
    property_ids = fields.One2many(
        'estate.property.model',   
        'sales_person_id',        
        string='Properties',
        domain=[('state', '=', 'new')]
    )
