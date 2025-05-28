class CompteBancaire:
    def __init__(self, numero: str, nom: str, solde: int):
        self.numero = numero
        self.nom = nom
        self.solde = solde

    def Versement(self, montant):
        if montant > 0:
            self.solde += montant
            print(f"Déposé: {montant}. Nouveau solde: {self.solde}")
        else:
            print("Le montant doit être positif.")

    def Retrait(self, montant):
        if 0 < montant <= self.solde:
            self.solde -= montant
            print(f"Retiré: {montant}. Nouveau solde: {self.solde}")
        else:
            print("Montant invalide ou fonds insuffisants.")

    def Agios(self):
        self.solde -= self.solde * 0.05
        print(f"Agios appliqués, nouveau solde: {self.solde}")
        
    def Afficher(self):
        print(f"Compte {self.numero} - Titulaire: {self.nom} - Solde: {self.solde}")
        