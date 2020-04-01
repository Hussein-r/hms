from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import models, fields
from odoo import api
import re
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = "hms.patient"
    First_Name = fields.Char("First Name", required=True)
    Last_Name = fields.Char("Last Name", required=True)
    Birth_Date = fields.Date("Birth Date")
    email = fields.Char("Email")
    History = fields.Html("History")
    CR_Ratio = fields.Float("CR Ratio")
    Blood_Type = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('O', 'O'),
        ('AB', 'AB'),
    ])
    State = fields.Selection([
        ("Undetermined", "Undetermined"),
        ("Good", "Good"),
        ("Fair", "Fair"),
        ("Serious", "Serious")
    ], default="Undetermined")
    PCR = fields.Boolean(default=False)
    Image = fields.Binary(string="Image")
    Address = fields.Char("Address")
    Age = fields.Integer("Age", compute="_compute_age")
    dept_id = fields.Many2one(comodel_name="hms.department")
    doctors_id = fields.Many2many(comodel_name="hms.doctor")
    is_dept_selected = fields.Boolean(default=False)
    flag = fields.Boolean(default=False)
    logs_id = fields.One2many(comodel_name="hms.logs",inverse_name="patient_id")

    @api.multi
    def change_status(self):
        current_status = self.State
        new_state = ""
        if self.State == "Undetermined":
            self.State = "Good"
            new_state = "Good"
        elif self.State == "Good":
            self.State = "Fair"
            new_state = "Fair"
        elif self.State == "Fair":
            self.State = "Serious"
            new_state = "Serious"
        else:
            self.State = "Undetermined"
            new_state = "Undetermined"

        result = self.env['hms.logs'].create({
            'date': datetime.now(),
            'description': "Changed State from " + current_status + "To " + new_state,
            'patient_id': self.id
        })
        return result

    @api.onchange('Age')
    def _onchange_age(self):
        if self.Age < 30 and self.Age != 0:
            self.PCR = True
            return ({
                'warning': {'title': 'Note', 'message': 'it has been checked'}
            })

    @api.onchange('dept_id')
    def select_dept(self):
        if self.flag:
            self.is_dept_selected = True
        self.flag = True



    @api.onchange('email')
    def validate_mail(self):
        if self.email:
            match = re.match('[^@]+@[^@]+\.[^@]+', self.email)
            if match is None:
                raise ValidationError('Not a valid E-mail')

    _sql_constraints = [
        ('email_unique', 'unique(email)', 'Please enter Unique Email')
    ]

    @api.one
    @api.depends('Birth_Date')
    def _compute_age(self):
        self.Age = relativedelta(datetime.now().date(), fields.Datetime.from_string(self.Birth_Date)).years

