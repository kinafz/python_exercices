class Gateau:
    def __init__(
        self,
        nom: str,
        temps_cuisson: int,
        list_ingredients: list[str],
        etapes_recette: list[str],
        createur: str
    ):
        self.nom = nom
        self.temps_cuisson = temps_cuisson
        self.list_ingredients = list_ingredients
        self.etapes_recette = etapes_recette
        self.createur = createur

    def display_ingredients(self):
        print(f"Ingrédients pour {self.nom} :")
        for ingredient in self.list_ingredients:
            print(f"- {ingredient}")
            
    def display_etapes(self):
        print(f"Étapes de la recette pour {self.nom} :")
        for i, etape in enumerate(self.etapes_recette, start=1):
            print(f"{i}. {etape}")