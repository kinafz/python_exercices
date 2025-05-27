### **TP 3**

---

### **Contexte :**

Tu travailles dans une équipe DevOps. L’entreprise gère des **déploiements d’environnements applicatifs** (dev, staging, prod). Chaque déploiement :

* Se base sur une version d'application
* Doit être enregistré (base de données)
* Est soumis à un **système de validation** (QA, sécurité)
* Peut être annulé en cas d’erreur
* Doit garantir **la cohérence de l’état final** (transaction)

---

* Créer une application CLI qui :

  * Gère des versions applicatives (`releases`)
  * Planifie des déploiements
  * Valide, exécute ou annule des déploiements
* Implémente la logique de déploiement comme une **transaction**
* Fournit une **commande de rollback** (annulation transactionnelle)


---

## **Modèle SQL :**

### `releases`

```sql
id INT PRIMARY KEY AUTO_INCREMENT,
version VARCHAR(50),
tag_git VARCHAR(50),
date_creation DATETIME
```

### `environnements`

```sql
id INT PRIMARY KEY AUTO_INCREMENT,
nom VARCHAR(50) UNIQUE CHECK (nom IN ('dev', 'staging', 'prod'))
```

### `deploiements`

```sql
id INT PRIMARY KEY AUTO_INCREMENT,
id_release INT,
id_env INT,
etat ENUM('planifié', 'validé', 'en_cours', 'réussi', 'échec', 'annulé'),
date_deploiement DATETIME,
FOREIGN KEY (id_release) REFERENCES releases(id),
FOREIGN KEY (id_env) REFERENCES environnements(id)
```


---

## **Cas transactionnel clé à implémenter :**

### **Valider et exécuter un déploiement**

1. Vérifie que l’environnement n’a **pas déjà un déploiement en cours**
2. Passe `etat` de `planifié` → `en_cours`
3. Simule l’exécution du déploiement (sleep + aléatoire ou commande réelle)
4. Si réussite :

   * passe à `réussi`
   * écrit dans `audit_logs`
5. Si échec :

   * rollback : remet `etat = planifié` ou `annulé`
   * log l’erreur

---

## **Fonctionnalités CLI à fournir :**

* `python main.py release --create 1.0.2 --tag v1.0.2`
* `python main.py deploy --release 1 --env prod`
* `python main.py validate --deploy-id 3`
* `python main.py status --env prod`
* `python main.py rollback --deploy-id 3`

