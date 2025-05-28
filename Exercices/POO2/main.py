import CompteBancaire

def main():
    compteBancaire = CompteBancaire.CompteBancaire("123456789", "Aurélien", 1000)

    compteBancaire.Afficher()
    compteBancaire.Versement(500)
    compteBancaire.Afficher()
    compteBancaire.Retrait(200)
    compteBancaire.Afficher()
    compteBancaire.Agios()
    compteBancaire.Afficher()

if __name__ == "__main__":
    main()