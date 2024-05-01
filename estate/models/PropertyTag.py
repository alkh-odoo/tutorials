from odoo import fields ,models

class PropertyType(models.Model):
    _name="estate.property.tag"
    _description="The tags of properties"
    _order = "name"
    name = fields.Char('Property tag', required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'Tag name has to be unique!')
    ]

