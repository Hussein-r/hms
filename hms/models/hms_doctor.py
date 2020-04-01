from odoo import models,fields

class HospitalDoctor(models.Model):
    _name = "hms.doctor"
    _rec_name = "First_Name"
    First_Name = fields.Char("First Name")
    Last_Name = fields.Char("Last Name")
    Image = fields.Binary("Doctor Image")