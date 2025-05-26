## TP : **Système de gestion de tickets de support (Helpdesk)**

### Objectif :

Créer une application CLI en Python permettant de **gérer des tickets de support** (incident/bug/demande).

---

## Description fonctionnelle :

### Table : `tickets`

| Champ           | Description                   |
| --------------- | ----------------------------- |
| `id`            | Identifiant auto-incrémenté   |
| `titre`         | Résumé du ticket              |
| `description`   | Détail de la demande          |
| `priorite`      | "faible", "moyenne", "haute"  |
| `statut`        | "ouvert", "en cours", "fermé" |
| `date_creation` | Date de création              |

---

## Fonctionnalités attendues (CRUD) :

### 1. **Créer un ticket**

* L’utilisateur saisit le titre, description, priorité.
* Statut par défaut : "ouvert"
* Date automatique (datetime.now)

### 2. **Lire les tickets**

* Afficher tous les tickets (id, titre, priorité, statut, date)
* Affichage lisible en tableau/ligne

### 3. **Mettre à jour un ticket**

* Modifier **priorité** ou **statut** d’un ticket donné par ID.

### 4. **Supprimer un ticket**

* Supprimer un ticket définitivement par son ID.
