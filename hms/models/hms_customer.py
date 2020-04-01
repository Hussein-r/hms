from odoo import models, fields
from odoo import api
from odoo.exceptions import ValidationError,UserError


class Customer(models.Model):
    _inherit = ['res.partner']
    related_patient_id = fields.Many2one(comodel_name='hms.patient')

    @api.constrains("email")
    def validate_customer_patient_email(self):
        if len(self.env['hms.patient'].search([("email", "=", self.email)], limit=1)) != 0:
            raise ValidationError('Sorry This Email Already Exists')

    @api.multi
    def unlink(self):
        for record in self:
            if record.related_patient_id:
                raise UserError("Sorry You Can't Delete This Customer Because it's Linked to Patient")
        super().unlink()
