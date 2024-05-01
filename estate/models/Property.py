from odoo import fields ,models, api, exceptions
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_is_zero, float_compare

class Property(models.Model):
    _name = "estate.property"
    _description = "This is a small testing setup :P"
    _order = "id desc"

    garden = fields.Boolean(default = False)
    total_area = fields.Float(compute="_compute_total_area")
    living_area = fields.Float()
    garden_area = fields.Float()


    best_price = fields.Float(compute="_best_price_compute")

    offer_ids = fields.One2many("estate.property.offer", string="offer", inverse_name = "property_id",)
    tag_ids = fields.Many2many("estate.property.tag",string="tags",required = True)

    buyer_id= fields.Many2one("res.partner",string="Buyer")
    sales_person_id = fields.Many2one("res.users",string="Sales person")
    type_id = fields.Many2one("estate.property.type",string="type", required = True)
    
    name = fields.Char('Plan Name', required=True, translate=True)
    description = fields.Text()
    active = fields.Boolean(default=True)
    postcode = fields.Char()
    date_availability = fields.Date(default = fields.Date.add(fields.Date.today(), months = 3) ,copy=False)
    expected_price = fields.Float(string= "expected_price", required=True)

    selling_price = fields.Float(string= "selling_price", readonly = True, copy=False)
    bedrooms = fields.Integer(default=2)
    garage = fields.Boolean()
    state = fields.Selection(
        string='state',
        selection=[('new','New'), ('recieved','Recieved'), ('accepted','Accepted'),('sold','Sold'),('canceled','Canceled')]
        , default = 'new')

    orientation = fields.Selection(
        string = "Orientation",
        selection = [('north','North'),('east','East'),('west','West')],
        copy = False,
    )
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >= 0)',''),
        ('check_selling_price','CHECK(selling_price >= 0)',''),
    ]

    def action_cancel(self):
        for record in self:
            if(record.state != 'sold'):
                record.state = 'canceled'
            else:
                raise UserError("You cannot cancel a sold property.")
        return True
    
    def action_sold(self):
        for record in self:
            if(record.state != 'canceled'):
                record.state = 'sold'
            else:
                raise UserError("You cannot set a canceled property as sold.")
        return True

    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.depends("offer_ids.price")
    def _best_price_compute(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0) 
        
    @api.onchange('garden')
    def onchange_check_validity(self):
        for record in self:
            if(record.garden):
                record.garden_area = 10
                record.orientation = 'north'
            else:
                record.garden_area = 0
                record.orientation = ''
    @api.constrains('expected_price','selling_price')
    def Check_(self):
        for record in self:  
            if not float_is_zero(record.expected_price, 2) and not float_is_zero(record.selling_price,2): 
                if float_compare(((record.selling_price)/(record.expected_price)),0.90,2) == -1:
                    raise ValidationError("Price is lower than 90%")                
                else:
                    record.property_id.selling_price = record.price
    @api.ondelete(at_uninstall=False)
    def _check_ondelete(self):
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise ValidationError(f"Cannot delete property '{record.name}' as its state is not 'New' or 'Canceled'.")

