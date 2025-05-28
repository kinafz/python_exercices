from Gateau import Gateau
def main():
    gateau = Gateau(
        nom="Gâteau au chocolat",
        temps_cuisson=30,
        list_ingredients=["200g de chocolat", "100g de sucre", "3 œufs", "50g de beurre"],
        etapes_recette=[
            "Préchauffez le four à 180°C.",
            "Faites fondre le chocolat et le beurre.",
            "Mélangez les œufs et le sucre.",
            "Incorporez le mélange chocolat-beurre.",
            "Versez dans un moule et enfournez."
        ],
        createur="Chef Pierre"
    )
    
    gateau.display_ingredients()
    gateau.display_etapes()

if __name__ == "__main__":
    main()