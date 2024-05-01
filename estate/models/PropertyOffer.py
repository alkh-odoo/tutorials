from odoo import fields ,models,api, tools
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.exceptions import UserError, ValidationError

class PropertyOffer(models.Model):
    # _inherit = 'res.users'
    _name="estate.property.offer"
    _description="The offer of properties"
    _order="price desc"
    price = fields.Float('Offered Price')

    property_type_id = fields.Many2one(
        string="Property Type",
        related='property_id.type_id', 
        store=True,  
        readonly=True  
    )  

    partner_id = fields.Many2one("res.partner",string="partner")
    
    property_id = fields.Many2one("estate.property", string="property")
    validity = fields.Integer(default=7)
    create_date = fields.Date(default= fields.Date.today(), readonly=True)
    date_deadline = fields.Date(compute ="_compute_deadline", inverse="_inverse_compute_deadline")

    
    status = fields.Selection(
        string = "offer status",
        selection = [('accepted','Accepted'),('refused','Refused')],
        copy = False
    )
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price >= 0)',''),
        ]
    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            if(record.create_date != None):
                record.date_deadline = fields.Date.add(record.create_date, days = record.validity)
    @api.model
    def create(self, vals):
        property_object_bestprice = self.env['estate.property'].browse(vals['property_id']).best_price
        if float_compare(vals['price'],property_object_bestprice,3) == -1:
            raise ValidationError(f"Cannot create offer with a price {property_object_bestprice}")
        return super(PropertyOffer,self).create(vals)


    def _inverse_compute_deadline(self):
        for record in self:
            record.date_deadline = record.date_deadline

    def confirm_offer(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.selling_price = record.price

    def deny_offer(self):
        for record in self:
            record.status = 'refused'