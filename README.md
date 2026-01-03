
# Gestion de Réservation d'Équipement (Odoo)
Ce projet est un module Odoo conçu pour gérer efficacement les réservations d'équipements au sein d'une organisation. Il permet de centraliser le parc matériel, de gérer les disponibilités et d'éviter les conflits de réservation.
##  Fonctionnalités Clés
###  Gestion du Matériel
- **Fiches Équipements** : Création et gestion d'équipements avec nom, code interne, description et capacité.
- **Suivi d'Activité** : Indicateur dynamique du nombre total de réservations par équipement.
- **Action Rapide** : Bouton direct pour créer une réservation depuis la fiche équipement.
###  Réservations
- **Planification Intuitive** : Gestion des dates de début et de fin avec calcul automatique de la durée.
- **Validation Intégrée** : Système anti-chevauchement empêchant de réserver le même matériel sur des créneaux identiques.
- **États de workflow** : Cycle de vie complet (Brouillon -> Confirmée -> Terminée -> Annulée).
- **Vues Multiples** : Visualisation en Liste, Formulaire et **Calendrier** pour une meilleure visibilité globale.
##  Architecture Technique
- **Modèles Odoo** :
  - `gestion_reservation.equipment` : Gestion du parc matériel.
  - `gestion_reservation.reservation` : Logique de réservation et contraintes métier.
- **Sécurité** : Gestion des droits d'accès via des groupes et fichiers CSV (`ir.model.access.csv`).
- **Interface** : Vues XML personnalisées, menus structurés et icônes d'application.
- **Données** : Séquences automatiques pour les références de réservation et données de démonstration incluses.

