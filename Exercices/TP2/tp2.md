
## TP 2

---

Créer une application Python (en ligne de commande) qui permet de gérer :

* Des **utilisateurs**
* Des **livres**
* Des **emprunts**
* Et d’afficher les **emprunts actifs** en liant les données des trois tables avec des **jointures SQL** exécutées depuis Python.

---

- 3 tables :

* `utilisateurs(id, nom, email)`
* `livres(id, titre, auteur)`
* `emprunts(id, id_utilisateur, id_livre, date_emprunt, date_retour)`

---


1. Ajouter un utilisateur
2. Ajouter un livre
3. Enregistrer un emprunt
4. Afficher tous les **emprunts en cours**, avec :

   * le nom de l’utilisateur
   * le titre du livre
   * la date d’emprunt
   * (→ en utilisant une **jointure entre les 3 tables**)
5. Afficher l’historique des livres empruntés par un utilisateur donné

---
