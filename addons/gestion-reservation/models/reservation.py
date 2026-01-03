# addons/gestion_reservation/models/reservation.py
from odoo import models, fields, api, exceptions
from datetime import timedelta

class Reservation(models.Model):
    _name = "gestion_reservation.reservation"
    _description = "Réservation d'équipement"
    _order = "start_datetime desc"

    name = fields.Char(string="Référence", required=True, default="New")
    equipment_id = fields.Many2one('gestion_reservation.equipment', string="Équipement", required=True)
    user_id = fields.Many2one('res.users', string="Utilisateur", default=lambda self: self.env.user)
    start_datetime = fields.Datetime(string="Début", required=True)
    end_datetime = fields.Datetime(string="Fin", required=True)
    duration_hours = fields.Float(string="Durée (h)", compute="_compute_duration", store=True)
    
    # Nouveaux champs demandés
    purpose = fields.Char(string="Objet de la réservation")
    attendee_count = fields.Integer(string="Nombre de participants")

    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('confirmed', 'Confirmée'),
        ('done', 'Terminée'),
        ('cancel', 'Annulée')
    ], default='draft', string="Statut")
    notes = fields.Text(string="Notes")

    @api.depends('start_datetime', 'end_datetime')
    def _compute_duration(self):
        for rec in self:
            if rec.start_datetime and rec.end_datetime:
                delta = rec.end_datetime - rec.start_datetime
                rec.duration_hours = round(delta.total_seconds() / 3600.0, 2)
            else:
                rec.duration_hours = 0.0

    @api.constrains('start_datetime', 'end_datetime', 'equipment_id')
    def _check_dates(self):
        for rec in self:
            if not rec.start_datetime or not rec.end_datetime:
                continue
            if rec.start_datetime >= rec.end_datetime:
                raise exceptions.ValidationError("La date de début doit être antérieure à la date de fin.")
            # Vérifier chevauchement (ignorer annulées et s'exclure soi-même)
            domain = [
                ('equipment_id', '=', rec.equipment_id.id),
                ('id', '!=', rec.id),
                ('state', '!=', 'cancel'),
                ('start_datetime', '<', rec.end_datetime),
                ('end_datetime', '>', rec.start_datetime),
            ]
            overlapping = self.search(domain)
            if overlapping:
                raise exceptions.ValidationError("Chevauchement détecté : cette réservation entre en conflit avec une autre réservation pour le même équipement.")

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancel'})

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('gestion_reservation.reservation') or 'New'
        return super(Reservation, self).create(vals_list)
