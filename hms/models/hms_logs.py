from odoo import models,fields
from datetime import datetime, timedelta


class HospitalLogs(models.Model):
    _name = "hms.logs"
    created_by = fields.Many2one('res.users', 'Current User', default=lambda self: self.env.user)
    date = fields.Date()
    description = fields.Text(string="Description")
    patient_id = fields.Many2one(comodel_name="hms.patient")