from odoo import fields ,models, _

class PropertyType(models.Model):
    _name="estate.property.type"
    _description="The types of"
    _order = "name"
    
    offer_count = fields.Integer(compute = "_compute_offer_count")
    offer_ids = fields.One2many('estate.property.offer', string='offers',inverse_name= "property_type_id")

    name = fields.Char('Property type', required=True)
    property_ids = fields.One2many("estate.property", string="property",inverse_name="type_id")
    _sql_constraints = [
        ('unique_code', 'unique(name)', '')
    ]
    
    def action_view_offers(self):

        return {
            "type": "ir.actions.act_window",
            "res_model": "estate.property.offer",
            "domain": [('id', 'in', self.offer_ids.ids)],
            "name": _("Offers"),
            'view_mode': 'tree,form',
        }
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

