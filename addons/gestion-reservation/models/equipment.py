# addons/gestion_reservation/models/equipment.py
from odoo import models, fields, api
class Equipment(models.Model):
    _name = "gestion_reservation.equipment"
    _description = "Équipement à réserver"

    name = fields.Char(string="Nom", required=True)
    code = fields.Char(string="Code", help="Code interne")
    description = fields.Text(string="Description")
    active = fields.Boolean(string="Actif", default=True)
    capacity = fields.Integer(string="Capacité", default=1)
    reservation_count = fields.Integer(string="Nombre réservations", compute="_compute_reservation_count")

    @api.depends()
    def _compute_reservation_count(self):
        for rec in self:
            rec.reservation_count = self.env['gestion_reservation.reservation'].search_count([('equipment_id', '=', rec.id)])

    def action_create_reservation(self):
        """Ouvre le formulaire de création de réservation pour cet équipement."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Nouvelle Réservation',
            'res_model': 'gestion_reservation.reservation',
            'view_mode': 'form',
            'context': {'default_equipment_id': self.id},
            'view_id': False,
            'target': 'current',
        }
